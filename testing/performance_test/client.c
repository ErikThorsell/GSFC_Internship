/* The original code for this client can be found here:
 * http://www.cs.rpi.edu/~moorthy/Courses/os98/Pgms/client.c */
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

// Static variables
static int sockfd;


/* This function is called when a system call fails. It displays a message about
 * the error on stderr and then aborts the program. */
void error(char *msg)
{
    perror(msg);
    exit(0);
}

/* Callable function from Fortran, used by calcf.f90, to connect to a server.
 */
int client(char *ipaddr, int in_portno)
{
    int portno;

    struct sockaddr_in serv_addr;
    struct hostent *server;

    portno = in_portno;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");

    server = gethostbyname(ipaddr);
    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(0);
    }

    memset(((char *) &serv_addr), 0, (sizeof(serv_addr)));
    serv_addr.sin_family = AF_INET;
    memcpy(((char *)server->h_addr),
           ((char *)&serv_addr.sin_addr.s_addr),
           (server->h_length));
    serv_addr.sin_port = htons(portno);

    if (connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr)) < 0) 
        error("ERROR connecting");

    //close(sockfd);

    return 0;
}

/* Callable function from Fortran, used by calcf.f90, as a calculator.
 * calc passes the query stored in buffer to server and returns the
 * answer. */
int *calc(int *indata, int length)
{

    int n;
    n = write(sockfd, indata, sizeof(int)*length);
    if (n < 0) 
         error("ERROR writing to socket");

    n = read(sockfd, indata, sizeof(int)*length);
    if (n < 0) 
        error("ERROR reading from socket");

    return indata;
}

