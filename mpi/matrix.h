#ifndef __MATRIX_H__
#define __MATRIX_H__

typedef struct {
  int rows;
  int cols;
  float **data;
} matrix;

void error(char *str);
matrix *alloc_matrix(int r, int c);
matrix *read_matrix(char *filename);
void print_patrix(matrix *m, FILE *f);

#endif
