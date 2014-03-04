#include <stdio.h>
#include <stdlib.h>
#include "matrix.h"

void error(char *str) {
  printf("%s\n", str);
  exit(1);
}

matrix *alloc_matrix(int r, int c) {
  int i;
  matrix *m = malloc(sizeof(matrix));
  if ((m->data = malloc(r * sizeof(float *))) == NULL) {
    error("Memory error.");
  }
  for (i = 0; i < r; i++) {
    if ((m->data[i] = malloc(c * sizeof(float))) == NULL) {
      error("Memmory error.");
    }
  }
  m->rows = r;
  m->cols = c;

  return m;
}

matrix *read_matrix(char *filename) {
  int c, r, i, j;
  FILE *f;
  matrix *m;
  float element;
  
  if ( (f = fopen(filename, "r")) == NULL) {
    error("Unable to open file.");
  }

  if (fscanf(f, "%d", &r) != 1) {
    error("Couldn't read number of rows.");
  }

  if (fscanf(f, "%d", &c) != 1) {
    error("Couldn't read number of column.");
  }

  m = alloc_matrix(r, c);

  for (i = 0; i < r; i++) {
    for (j = 0; j < c; j++) {
      if (fscanf(f, "%f", &element) != 1) {
	error("Couldn't read element");
      }
      m->data[i][j] = element;
    }
  }
  
  fclose(f);    
  return m;
}

void print_matrix(matrix *m, FILE *f) {
  int i,j;
  fprintf(f, "%d\n%d\n", m->rows, m->cols);
  for (i = 0; i < m->rows; i++) {
    for (j = 0; j < m->cols; j++) {
      fprintf(f, "%f\n", m->data[i][j]);
    }
  }
}
