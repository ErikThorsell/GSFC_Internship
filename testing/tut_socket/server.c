#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <time.h> 

int main(int argc, char *argv[])
{
    int listenfd = 0, connfd = 0;
    struct sockaddr_in serv_addr;

    char sendBuff[1025];
    time_t ticks; 

    /* socket(domain, type, protocol) creates an UN-named socket inside the
     * kernel and returns an integer known as socket descriptor.
     * AF_INET == IPV4
     * SOCK_STREAM provides sequenced reliable, two-way, connection-based byte
     * streams.
     * The protocol specifies a particular protocol to be used with the socket.
     * Normally only a single protocol exists to support a particular socket
     * type within a given protocol family, in which case protocol can be
     * specified as 0. */
    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    memset(&serv_addr, '0', sizeof(serv_addr));
    memset(sendBuff, '0', sizeof(sendBuff)); 

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(5000); 

    /* When a socket is created with socket(), it exists in a name space
     * (address family) but has no address assigned to it.
     * bind(sockfd, addr, addrlen) assigns the address specified by addr to the
     * socket referred to by the file descriptor sockfd. addrlen specifies the
     * size, in bytes, of the address structure pointed to by addr. */
    bind(listenfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr));

    /* listen(sockfd, backlog) marks the socket referred to by sockfd as a
     * passive socket, that is, as a socket that will be used to accept
     * incoming connection requests using accept(2).
     * The sockfd argument is a file descriptor that refers to a socket of type
     * SOCK_STREAM or SOCK_SEQPACKET.
     * The backlog argument defines the maximum length to which the queue of
     * pending connections for sockfd may grow.*/
    listen(listenfd, 10);

    /*
     *  We know have a working server socket!
     */

    while(1) {
        /* The accept(sockfd, addr, addrlen) system call is used with
         * connection-based socket types (SOCK_STREAM, SOCK_SEQPACKET). It
         * extracts the first connection request on the queue of pending
         * connections for the listening socket, sockfd, creates a new
         * connected socket, and returns a new file descriptor referring to
         * that socket. The newly created socket is not in the listening state.
         * The original socket sockfd is unaffected by this call.
         * In the call to accept(), the server is put to sleep and when for an
         * incoming client request, the three way TCP handshake* is complete,
         * the function accept () wakes up and returns the socket descriptor
         * representing the client socket.*/
        connfd = accept(listenfd, (struct sockaddr*)NULL, NULL); 

        ticks = time(NULL);
        snprintf(sendBuff, sizeof(sendBuff), "%.24s\r\n", ctime(&ticks));
        write(connfd, sendBuff, strlen(sendBuff));

        close(connfd);
        sleep(1);
     }
}
