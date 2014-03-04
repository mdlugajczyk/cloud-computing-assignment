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

int main() {
  matrix *l = read_matrix("m1.txt");
  matrix *r = read_matrix("m2.txt");
  matrix *mul = multiply(l, r);
  print_matrix(l, stdout);
  printf("\n");
  print_matrix(r,stdout);
  printf("\n");
  print_matrix(mul, stdout);
  
  return 0;
}
