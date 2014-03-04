#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "matrix.h"

/*
 * Returns random float from interval [0,100]
 */
float random_float() {
  return 100*(float)rand()/RAND_MAX;
}

matrix *random_matrix(int rows, int cols) {
  int i,j;
  matrix *m = alloc_matrix(rows, cols);

  for (i = 0; i < rows; i++) {
    for (j = 0; j < cols; j++) {
      m->data[i][j] = random_float();
    }
  }
    
  return m;
}

int main(int argc, char **argv) {
  int rows, cols;
  matrix *m;
  srand(time(NULL));
  
  if (argc != 3) {
    printf("Usage: %s rows cols\n", argv[0]);
    return 1;
  }

  rows = atoi(argv[1]);
  cols = atoi(argv[2]);
  m = random_matrix(rows, cols);
  print_matrix(m, stdout);

  return 0;
}
