/* This is the child part of the posix parent/child (producer/consumer)
 * program. The child will look for a designated file in memory and read the
 * content of that file.
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/shm.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <errno.h>
#include <string.h>

void display(char *prog, char *bytes, int n);
void initConsumer(char* name);
void mapConsumer(int size);
void terminateConsumer(int size, char* name);
char* readFromMem();
int fd;
char* shm_base;

/* ************************************************************************* 
int main(void)
{
    char *name = "/shm-example";
    int size, fd;	
    char *shm_base;

    size = 4096;

    fd = initConsumer(name);
    shm_base = mapConsumer(fd, size);
    readFromMem(shm_base);
    terminateConsumer(shm_base, fd, size, name);

    return 0;
}

 ************************************************************************* */

//int initConsumer(char* name){
void initConsumer(char* name){
    //int fd;
    printf("C: filename is: %s\n", name);
    fd = shm_open(name, O_RDWR, 0666);
    if (fd == -1) {
        printf("prod: Shared memory failed: %s\n", strerror(errno));
        exit(1);
    }

    //return fd;
}

//char* mapConsumer(int fd, int size){
void mapConsumer(int size){
    //char* shm_base;

    shm_base = mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (shm_base == MAP_FAILED) {
        printf("prod: Map failed: %s\n", strerror(errno));
        exit(1);
    }

    //return shm_base;
}

//void terminateConsumer(char* shm_base, int fd, int size, char* name) {
void terminateConsumer(int size, char* name) {

    if (munmap(shm_base, size) == -1) {
        printf("prod: Unmap failed: %s\n", strerror(errno));
        exit(1);
    }

    if (close(fd) == -1) {
        printf("prod: Close failed: %s\n", strerror(errno));
        exit(1);
    }

    if (shm_unlink(name) == -1) {
        printf("cons: Error removing %s: %s\n", name, strerror(errno));
        exit(1);
    }
}

char* readFromMem() {
     printf("C: I read from base: %s\n", shm_base);

    return *shm_base;
}

void display(char* prog, char* bytes, int n)
{
    printf("display: %s\n", prog);
    for (int i = 0; i < n; i++) {
        printf("%02x%c", bytes[i], ((i+1)%16) ? ' ' : '\n'); 
    }
    printf("\n");
}

