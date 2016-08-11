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
//int initProducer(char* name, int size);
void initProducer(char* name, int size);
//char* mapProducer(int shm_fd, int size);
void mapProducer(int size);
//void terminateProducer(char* shm_base, int shm_fd, int size);
void terminateProducer(int size);
//void writeToMem(char * base, char * msg);
void writeToMem(char * msg);
char* shm_base;
int shm_fd;
/* ************************************************************************* 

int main(void)
{
    char* name = "/shm-example";
    char* message = "Why split the strings? Isn't there enough room?";
    int size, shm_fd;
    //char* shm_base;
    //char* mock_base = "Why split the strings? Isn't there enough room?";
    
    size = 4096;

    shm_fd = initProducer(name, size);
    shm_base = mapProducer(shm_fd, size);
    writeToMem(shm_base, message);
    terminateProducer(shm_base, shm_fd, size);
    printf("And that's it! Tallyho!\n");
    return 0;
}

 ************************************************************************* */

//int initProducer(char* name, int size){
void initProducer(char* name, int size){

    shm_fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        printf("prod: Shared memory failed: %s\n", strerror(errno));
        exit(1);
    }

    ftruncate(shm_fd, size);
    
    //return shm_fd;
}

//char* mapProducer(int shm_fd, int size){
void mapProducer(int size){
    // char* shm_base;
    shm_base = mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shm_base == MAP_FAILED) {
        printf("prod: Map failed: %s\n", strerror(errno));
        exit(1);
    }

    //return shm_base;
}

//void terminateProducer(char* base, int shm_fd, int size) {
void terminateProducer(int size) {

    printf("C: Base: %s\n", shm_base);
    printf("C: FD: %d\n", shm_fd);
    printf("C: Size: %d\n", size);

    if (munmap(shm_base, size) == -1) {
        printf("prod: Unmap failed: %s\n", strerror(errno));
        exit(1);
    }

    if (close(shm_fd) == -1) {
        printf("prod: Close failed: %s\n", strerror(errno));
        exit(1);
    }
}

//void writeToMem(char* base, char* msg) {
void writeToMem(char* msg) {
    char* ptr;

    printf("C: Base in writeToMem: %s\n", shm_base);
    printf("C: Msg received from Fortran: %s\n", msg);

    ptr = shm_base;
    //printf(ptr, "%s\n");
    ptr += sprintf(ptr, "%s", msg);
    printf("C: Base in writeToMem, after writing: %s\n", shm_base);
}

void display(char* prog, char* bytes, int n)
{
    printf("display: %s\n", prog);
    for (int i = 0; i < n; i++) {
        printf("%02x%c", bytes[i], ((i+1)%16) ? ' ' : '\n'); 
    }
    printf("\n");
}
