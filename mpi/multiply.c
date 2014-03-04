#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include "matrix.h"

matrix *multiply(matrix *a, matrix *b) { 
  int i,j,k;
  matrix *result = alloc_matrix(a->rows, b->cols);

  for (i = 0; i < result->rows; i++) {
    for (j = 0; j < result->cols; j++) {
      double sum = 0;
      for (k = 0; k < a->cols; k++) {
	sum += a->data[i][k] * b->data[k][j];
      }
      result->data[i][j] = sum;
    }
  }

  return result;
}

void write_result(char *filename, matrix *m, double t) {
  FILE *f;
  if ((f = fopen(filename, "w")) == NULL) {
    error("Can't open output file %s.");
  }
  fprintf(f, "%f\n", t);
  print_matrix(m, f);
  fclose(f);
}

void read_input(int argc, char **argv, matrix **m1, matrix **m2) {
  if (argc != 4) {
    printf("Usage: %s input1 input2 output\n", argv[0]);
    exit(1);
  }

  *m1 = read_matrix(argv[1]);
  *m2 = read_matrix(argv[2]);
}

int problem_size_for_process(int rank, int size, int rows) {
  int row_slice = rows / size;
  int nodes_with_additional_slice = rows % size;

  if (rank < nodes_with_additional_slice) {
    row_slice++;
  }

  return row_slice;
}

/*
 * Sends relevant rows of first input matrix to all processes.
 * Rows are distributed equally, max differnece between received number of rows
 * between processes is 1.
 */
void distribute_first_matrix(int rank, int size, int rows, matrix *m) {
  int i, offset, current_proces_row_size;
  if (rank == 0) {
    for (i = 1, offset = problem_size_for_process(0, size, rows);
	 i < size;
	 i++, offset += current_proces_row_size) {
      current_proces_row_size = problem_size_for_process(i, size, rows);
      MPI_Send(m->data[offset],  current_proces_row_size * m->cols,
	       MPI_FLOAT, i, 0, MPI_COMM_WORLD);
    }
  } else {
    MPI_Recv(m->data[0], problem_size_for_process(rank, size, rows) * m->cols, MPI_FLOAT, 0, 0,
	     MPI_COMM_WORLD, NULL);
  }
}

matrix *gather_results(int rank, int size, int rows, int cols, matrix *partial_result) {
  int i, offset;
  int current_proces_row_size = problem_size_for_process(rank, size, rows);
  matrix *accumulated_result;
  if (rank == 0) {
    accumulated_result = alloc_matrix(rows, cols);
    for (i = 0 ; i < current_proces_row_size; i++)
      accumulated_result->data[i] = partial_result->data[i];
    
    for (i = 1, offset = current_proces_row_size;
	 i < size;
	 i++, offset += current_proces_row_size) {
      current_proces_row_size = problem_size_for_process(i, size, rows);
      MPI_Recv(accumulated_result->data[offset], current_proces_row_size * cols,
	       MPI_FLOAT, i, 0, MPI_COMM_WORLD, NULL);
    }
  } else {
    MPI_Send(partial_result->data[0], current_proces_row_size * cols,
	     MPI_FLOAT, 0, 0, MPI_COMM_WORLD);
  }
  
  return accumulated_result;
}

void broadcast_input_size(int *m1rows, int *m1cols, int *m2rows, int *m2cols) {
  MPI_Bcast(m1rows, 1, MPI_INT, 0, MPI_COMM_WORLD);
  MPI_Bcast(m1cols, 1, MPI_INT, 0, MPI_COMM_WORLD);
  MPI_Bcast(m2rows, 1, MPI_INT, 0, MPI_COMM_WORLD);
  MPI_Bcast(m2cols, 1, MPI_INT, 0, MPI_COMM_WORLD);
}

void mpi_multiply(int rank, int size, int argc, char **argv) {
  double start_time;
  matrix *m1, *m2, *result, *accumulated_result;
  int m1rows, m1cols;
  int m2rows, m2cols;
  int problem_size;

  if (rank == 0) {
    read_input(argc, argv, &m1, &m2);
    m1rows = m1->rows;
    m1cols = m1->cols;
    m2rows = m2->rows;
    m2cols = m2->cols;
    if (m1cols != m2rows) {
      error("Invalid matrix dimensions");
    }
    if (size > m1rows) {
      error("More compute nodes than problems to allocate.");
    }
  }

  start_time = MPI_Wtime();
  broadcast_input_size(&m1rows, &m1cols, &m2rows, &m2cols);
  problem_size = problem_size_for_process(rank, size, m1rows);
  
  if (rank == 0) {
    m1->rows = problem_size;
  } else {
    m1 = alloc_matrix(problem_size, m1cols);
    m2 = alloc_matrix(m2rows, m2cols);
  }

  distribute_first_matrix(rank, size, m1rows, m1);
  // Second matrix is send without partitioning, as it would require
  // copying it to temporary buffer. With maximum number of nodes 16, it shouldn't be a problem.
  MPI_Bcast(m2->data[0], m2rows * m2cols, MPI_FLOAT, 0, MPI_COMM_WORLD);
  result = multiply(m1, m2);
  accumulated_result = gather_results(rank, size, m1rows, m2cols, result);
				      
  if (rank == 0)
    write_result(argv[3], accumulated_result, MPI_Wtime() - start_time);
}

int main(int argc, char **argv) {
  int rank, size;
  
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  
  mpi_multiply(rank, size, argc, argv);
  
  MPI_Finalize();
  return 0;
}
