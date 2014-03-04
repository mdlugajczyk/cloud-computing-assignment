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
  if ((f = fopen(filename, "w+")) == NULL) {
    error("Can't open output file.");
  }
  fprintf(f, "%f\n", t);
  print_matrix(m, f);
  fclose(f);
}

int main(int argc, char **argv) {
  matrix *m1, *m2, *result;

  if (argc != 4) {
    printf("Usage: %s input1 input2 output\n", argv[0]);
    return 1;
  }

  m1 = read_matrix(argv[1]);
  m2 = read_matrix(argv[2]);
  result = multiply(m1, m2);
  write_result(argv[3], result, 0);
  return 0;
}
