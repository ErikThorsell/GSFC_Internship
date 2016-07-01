/* The original code for this server can be found here:
 * http://www.cs.rpi.edu/~moorthy/Courses/os98/Pgms/server.c */
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <math.h>
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
        int length = 100000;
        int indata[length];
        newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
        if (newsockfd < 0)
             error("ERROR on accept");

        // Here comes the query from client.c
        n = read(newsockfd, indata, sizeof(int)*length);
        if (n < 0) error("ERROR reading from socket");

        square(indata);

        // write returns the data to the client
        n = write(newsockfd, indata, sizeof(int)*length);

        if (n < 0) error("ERROR writing to socket");
    }

    return 0;

}
