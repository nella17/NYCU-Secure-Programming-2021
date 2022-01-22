#include <stdlib.h>

signed main() {
    char *A = (char *) malloc(0x2e);
    char *B = (char *) malloc(0x22);
    char *C = (char *) malloc(0x1d);
    char *D = (char *) malloc(0x25);
    char *E = (char *) malloc(0x11);
    char *F = (char *) malloc(0x23);
    char *G = (char *) malloc(0x19);
    free(E);
    free(F);
    free(B);
    free(G);
    free(C);
    free(D);
    free(A);
}
