#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
 
int main(void)
{
    const char *p = "10 200000000000000000000000000000 30 -40";
    printf("Parsing '%s':\n", p);
    char *end;
    int c = 1;

    for (long i = strtol(p, &end, 10); p != end; i = strtol(p, &end, 10))
    {
        printf("Run number: '%d'\n\n", c);
        printf("'%.*s' -> ", (int)(end-p), p);
        p = end;
        if (errno == ERANGE){
            printf("range error, got ");
            errno = 0;
        }
        printf("%ld\n", i);
        c++;
    }
}
