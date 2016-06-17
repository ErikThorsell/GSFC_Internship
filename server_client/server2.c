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

int main(int argc, char *argv[])
{
   /* sockfd and newsockfd are file descriptors, i.e. array subscripts into the
    * file descriptor table. These two variables store the values returned by the
    * socket system call and the accept system call.
    *
    * portno stores the port number on which the server accepts connections.
    *
    * clilen stores the size of the address of the client. This is needed for the
    * accept system call. */
    int sockfd, newsockfd, portno, clilen;

   /* The server reads characters from the socket connection into this
    * buffer. */
    char buffer[256];
    char *operator;

   /* A sockaddr_in is a structure containing an internet address. The
    * variable serv_addr will contain the address of the server, and cli_addr
    * will contain the address of the client which connects to the server. n
    * is the return value for the read() and write() calls; i.e. it contains
    * the number of characters read or written. */
    struct sockaddr_in serv_addr, cli_addr; int n;

   /* The user needs to pass in the port number on which the server will
    * accept connections as an argument. This code displays an error message
    * if the user fails to do this. */
    if (argc < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }

   /* The socket() system call creates a new socket. It takes three arguments.
    * The first is the address domain of the socket. Recall that there are two
    * possible address domains, the unix domain for two processes which share
    * a common file system, and the Internet domain for any two hosts on the
    * Internet. The symbol constant AF_UNIX is used for the former, and
    * AF_INET for the latter (there are actually many other options which can
    * be used here for specialized purposes).
    *
    * The second argument is the type of socket. Recall that there are two
    * choices here, a stream socket in which characters are read in a
    * continuous stream as if from a file or pipe, and a datagram socket, in
    * which messages are read in chunks. The two symbolic constants are
    * SOCK_STREAM and SOCK_DGRAM. The third argument is the protocol. If this
    * argument is zero (and it always should be except for unusual
    * circumstances), the operating system will choose the most appropriate
    * protocol. It will choose TCP for stream sockets and UDP for datagram
    * sockets.
    *
    * The socket system call returns an entry into the file descriptor table
    * (i.e. a small integer). This value is used for all subsequent references
    * to this socket. If the socket call fails, it returns -1. In this case
    * the program displays and error message and exits. However, this system
    * call is unlikely to fail. */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
       error("ERROR opening socket");

   /* The function bzero() sets all values in a buffer to zero. It takes two
    * arguments, the first is a pointer to the buffer and the second is the
    * size of the buffer. Thus, this line initializes serv_addr to zeros. */
    memset(((char *) &serv_addr), 0, (sizeof(serv_addr)));

   /* The port number on which the server will listen for connections is
    * passed in as an argument, and this statement uses the atoi() function
    * to convert this from a string of digits to an integer. */
    portno = atoi(argv[1]);

   /* The variable serv_addr is a structure of type struct sockaddr_in. This
    * structure has four fields. The first field is short sin_family, which
    * contains a code for the address family. It should always be set to the
    * symbolic constant AF_INET. */
    serv_addr.sin_family = AF_INET;

   /* The second field of serv_addr is unsigned short sin_port , which contain
    * the port number. However, instead of simply copying the port number to
    * this field, it is necessary to convert this to network byte order using
    * the function htons() which converts a port number in host byte order to
    * a port number in network byte order. */
    serv_addr.sin_addr.s_addr = INADDR_ANY;

   /* The third field of sockaddr_in is a structure of type struct in_addr
    * which contains only a single field unsigned long s_addr. This field
    * contains the IP address of the host. For server code, this will always
    * be the IP address of the machine on which the server is running, and
    * there is a symbolic constant INADDR_ANY which gets this address. */
    serv_addr.sin_port = htons(portno);

   /* The bind() system call binds a socket to an address, in this case the
    * address of the current host and port number on which the server will
    * run. It takes three arguments, the socket file descriptor, the address
    * to which is bound, and the size of the address to which it is bound.
    * The second argument is a pointer to a structure of type sockaddr, but
    * what is passed in is a structure of type sockaddr_in, and so this must
    * be cast to the correct type. This can fail for a number of reasons, the
    * most obvious being that this socket is already in use on this machine.*/
    if (bind(sockfd, (struct sockaddr *) &serv_addr,
             sizeof(serv_addr)) < 0) 
             error("ERROR on binding");

   /* The listen system call allows the process to listen on the socket for
    * connections. The first argument is the socket file descriptor, and the
    * second is the size of the backlog queue, i.e., the number of connections
    * that can be waiting while the process is handling a particular
    * connection. This should be set to 5, the maximum size permitted by most
    * systems. If the first argument is a valid socket, this call cannot fail,
    * and so the code doesn't check for errors.*/
    listen(sockfd,5);

   /* The accept() system call causes the process to block until a client
    * connects to the server. Thus, it wakes up the process when a connection
    * from a client has been successfully established. It returns a new file
    * descriptor, and all communication on this connection should be done using
    * the new file descriptor. The second argument is a reference pointer to
    * the address of the client on the other end of the connection, and the
    * third argument is the size of this structure. */
    clilen = sizeof(cli_addr);
    newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
    if (newsockfd < 0) 
         error("ERROR on accept");

   /* Note that we would only get to this point after a client has successfully
    * connected to our server. Note that the read call
    * uses the new file descriptor, the one returned by accept(), not the
    * original file descriptor returned by socket(). Note also that the read()
    * will block until there is something for it to read in the socket, i.e.
    * after the client has executed a write(). It will read either the total
    * number of characters in the socket or 255, whichever is less, and return
    * the number of characters read.*/
    memset((buffer),0,(256));
    n = read(newsockfd, buffer, 255);
    char *p = buffer;
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

    if(strncmp(operator, " add\n", 5) == 0)
    {

        for (int i = 0; i < array_length; i++)
        {
            sum += list[i];
        }
        char ans[255];
        strcat(ans, "The answer to the question is: ");
        sprintf(c_sum, "%d", sum);
        strcat(ans, c_sum);
        n = write(newsockfd, ans, 255);
    } else {
        n = write(newsockfd, "Sorry, I can only add. (Usage: 1 2 add)", 255);
    }

   /* Once a connection has been established, both ends can both read and write
    * to the connection. Naturally, everything written by the client will be
    * read by the server, and everything written by the server will be read by
    * the client. This code simply writes a short message to the client. The
    * last argument of write is the size of the message.*/
    if (n < 0) error("ERROR writing to socket");

   /* This terminates main and thus the program. Since main was declared to be
    * of type int as specified by the ascii standard, many compilers complain
    * if it does not return anything. */
    return 0;
}
