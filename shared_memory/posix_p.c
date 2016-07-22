/**
 * Simple program demonstrating shared memory in POSIX systems.
 *
 * This is the producer process that writes to the shared memory region.
 *
 * Figure 3.17
 *
 * @author Silberschatz, Galvin, and Gagne
 * Operating System Concepts - Ninth Edition
 * Copyright John Wiley & Sons - 2013
 *
 * modifications by dheller@cse.psu.edu, 31 Jan. 2014
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
int initializeMem(char* name, int size);
char* mapMemory(int shm_fd, int size);
void terminateMem(char* shm_base, int i, int size);
void writeToMem(char * base, char * msg);

/* ************************************************************************* */
int main(void)
{
    char* message = "Why split the strings? Isn't there enough room?";
    char* shm_base;
    int size, shm_fd;

    size = 4096;

    shm_fd = initializeMem("/shm-example", size);
    shm_base = mapMemory(shm_fd, size);

    display("prod", shm_base, 64);

    writeToMem(shm_base, message);
    display("prod", shm_base, 64);

    terminateMem(shm_base, shm_fd, size);

    return 0;
}

/* ************************************************************************* */

int initializeMem(char* name, int size){
    int shm_fd;		// file descriptor, from shm_open()

    shm_fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        printf("prod: Shared memory failed: %s\n", strerror(errno));
        exit(1);
    }

    /* configure the size of the shared memory segment */
    ftruncate(shm_fd, size);

    return shm_fd;
}

char* mapMemory(int shm_fd, int size){
    char* shm_base;

    /* map the shared memory segment to the address space of the process */
    shm_base = mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shm_base == MAP_FAILED) {
        printf("prod: Map failed: %s\n", strerror(errno));
        // close and shm_unlink?
        exit(1);
    }

    return shm_base;
}

void terminateMem(char* shm_base, int shm_fd, int size) {

    /* remove the mapped memory segment from the address space of the process */
    if (munmap(shm_base, size) == -1) {
        printf("prod: Unmap failed: %s\n", strerror(errno));
        exit(1);
    }

    /* close the shared memory segment as if it was a file */
    if (close(shm_fd) == -1) {
        printf("prod: Close failed: %s\n", strerror(errno));
        exit(1);
    }
}

void writeToMem(char * base, char * msg) {
    char* ptr;

    ptr = base;
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
