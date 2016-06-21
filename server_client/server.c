/* The original code for this server can be found here:
 * http://www.cs.rpi.edu/~moorthy/Courses/os98/Pgms/server.c
 * and the comments are taken from:
 * http://www.cs.rpi.edu/~moorthy/Courses/os98/Pgms/socket.html */
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

/* This function is called when a system call fails. It displays a message about
 * the error on stderr and then aborts the program. */
void error(char *msg)
{
    perror(msg);
    exit(1);
}

int server(int in_portno)
{
   int sockfd, newsockfd, portno, clilen;

    char buffer[256];
    char *operator;

    struct sockaddr_in serv_addr, cli_addr; int n;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
       error("ERROR opening socket");

    memset(((char *) &serv_addr), 0, (sizeof(serv_addr)));

    portno = in_portno;

    serv_addr.sin_family = AF_INET;

    serv_addr.sin_addr.s_addr = INADDR_ANY;

    serv_addr.sin_port = htons(portno);

    if (bind(sockfd, (struct sockaddr *) &serv_addr,
             sizeof(serv_addr)) < 0) 
             error("ERROR on binding");

    listen(sockfd,5);

    clilen = sizeof(cli_addr);
    newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
    if (newsockfd < 0) 
         error("ERROR on accept");

    memset((buffer),0,(256));
    n = read(newsockfd, buffer, 255);
    char *p = buffer;
    printf("Buffer: %s\n", buffer);
    if (n < 0) error("ERROR reading from socket");
    long list[2];
    long sum = 0;
    char c_sum[255];
    int array_length = 0;

    for (long i = strtol(p, &operator, 10); p != operator; i = strtol(p, &operator, 10))
    {
        list[array_length] = i;
        p = operator;
        if (errno == ERANGE)
        {
            printf("range error, got ");
            errno = 0;
        }
        array_length++;
    }

    printf("The operator is: %s", operator);
    if(strncmp(operator, " add", 4) == 0)
    {

        for (int i = 0; i < array_length; i++)
        {
            sum += list[i];
        }
        char ans[255];
        sprintf(ans, "%d", sum);
        n = write(newsockfd, ans, 255);
    } else {
        n = write(newsockfd, "Sorry, I can only add. (Usage: 1 2 add)", 255);
    }

    if (n < 0) error("ERROR writing to socket");

    return 0;
}
