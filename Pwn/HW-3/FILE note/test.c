#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>

int main() {
    struct stat buf;
    fstat(0, &buf);
    printf("%d", buf.st_blksize);
}
