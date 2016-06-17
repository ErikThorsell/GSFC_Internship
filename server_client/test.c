#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
 
int main(void)
{
    int i = 10;
    int *k;

    k = &i;

    printf("W/o *: '%ld'\n", k);
    printf("W/ *: '%ld'\n", *k);
    printf("W/ &: '%ld'\n", &k);
    printf("W/ & (i): '%ld'\n", &i);
}
