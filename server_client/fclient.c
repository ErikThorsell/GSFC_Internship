#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 


/*
int main()
{
    calc_("Hello world.", "localhost", 55555);
    return 0;
}
*/

void error(char *msg)
{
    perror(msg);
    exit(0);
}

int calc_(char *indata, char *ipaddr, int *in_portno)
{
    int sockfd, portno, n;

    struct sockaddr_in serv_addr;
    struct hostent *server;

    char buffer[256];
    //portno = *in_portno;
    portno = in_portno;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");

    //server = gethostbyname(*ipaddr);
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

    printf("ackd");
    memset((buffer), 0, (256));
    //strcpy(buffer, *indata);
    strcpy(buffer, indata);
    //fgets(buffer, 255, *indata);
    n = write(sockfd, buffer, strlen(buffer));
    if (n < 0) 
         error("ERROR writing to socket");
    memset((buffer), 0, (256));
    n = read(sockfd,buffer,255);
    if (n < 0) 
         error("ERROR reading from socket");
    printf("%s\n",buffer);
    return 0;
}
