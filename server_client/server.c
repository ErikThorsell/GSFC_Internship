/* The original code for this server can be found here:
 * http://www.cs.rpi.edu/~moorthy/Courses/os98/Pgms/server.c */
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

/* Callable function from Fortran, used by calcs.f90, to start a server that
 * can recieve queries. */
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

    while(1)
    {
        newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
        if (newsockfd < 0)
             error("ERROR on accept");

        memset((buffer),0,(256));

        // Here comes the query from client.c
        n = read(newsockfd, buffer, 255);
        if (n < 0) error("ERROR reading from socket");
        char *p = buffer;
        long list[2];
        long result = 0;
        char c_sum[255];
        int array_length = 0;

        // calculate is a function in calcs.f90 that interprets a query and
        // returns the answer
        result = calculate(p);

        char ans[255];
        sprintf(ans, "%d", result);

        // write returns the data to the client
        n = write(newsockfd, ans, 255);

        if (n < 0) error("ERROR writing to socket");
    }

    return 0;

}
