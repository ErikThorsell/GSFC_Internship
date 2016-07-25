/* This is the child part of the posix parent/child (producer/consumer)
 * program. The child will look for a designated file in memory and read the
 * content of that file.
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/shm.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <errno.h>

void display(char *prog, char *bytes, int n);
int initProducer(char* name, int size);
char* mapProducer(int shm_fd, int size);
void terminateProducer(char* shm_base, int shm_fd, int size);
void writeToMem(char * base, char * msg);

/* ************************************************************************* 
int main(void)
{
    char* name = "/shm-example";
    char* message = "Why split the strings? Isn't there enough room?";
    int size, shm_fd;
    char* shm_base;

    size = 4096;

    shm_fd = initProducer(name, size);
    shm_base = mapProducer(shm_fd, size);
    writeToMem(shm_base, message);
    terminateProducer(shm_base, shm_fd, size);

    return 0;
}

 ************************************************************************* */

int initProducer(char* name, int size){
    int shm_fd;

    shm_fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        printf("prod: Shared memory failed: %s\n", strerror(errno));
        exit(1);
    }

    ftruncate(shm_fd, size);

    return shm_fd;
}

char* mapProducer(int shm_fd, int size){
    char* shm_base;

    shm_base = mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shm_base == MAP_FAILED) {
        printf("prod: Map failed: %s\n", strerror(errno));
        exit(1);
    }

    return shm_base;
}

void terminateProducer(char* shm_base, int shm_fd, int size) {

    printf("Base: %s\n", shm_base);
    printf("FD: %d\n", shm_fd);
    printf("Size: %d\n", size);

    if (munmap(shm_base, size) == -1) {
        printf("prod: Unmap failed: %s\n", strerror(errno));
        exit(1);
    }

    if (close(shm_fd) == -1) {
        printf("prod: Close failed: %s\n", strerror(errno));
        exit(1);
    }
}

void writeToMem(char* base, char* msg) {
    char* ptr;

    printf("Base WTM: %s\n", base);
    printf("Msg: %s\n", msg);

    ptr = base;
    printf(ptr, "%s");
    ptr += sprintf(ptr, "%s", msg);
}

void display(char* prog, char* bytes, int n)
{
    printf("display: %s\n", prog);
    for (int i = 0; i < n; i++) {
        printf("%02x%c", bytes[i], ((i+1)%16) ? ' ' : '\n'); 
    }
    printf("\n");
}
