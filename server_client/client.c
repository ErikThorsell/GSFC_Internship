#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

// Static variables
static int sockfd;

void error(char *msg)
{
    perror(msg);
    exit(0);
}

int client(char *ipaddr, int in_portno)
{
    int portno;

    struct sockaddr_in serv_addr;
    struct hostent *server;

    printf("Port number is: %d\n", in_portno);
    portno = in_portno;
    printf("Port number2 is: %d\n", portno);
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

    return 0;
}

int calc(char *indata)
{
    char buffer[256];
    int n;
    int ans;
    memset((buffer), 0, (256));
    strcpy(buffer, indata);
    n = write(sockfd,buffer,strlen(buffer));
    if (n < 0) 
         error("ERROR writing to socket");
    memset((buffer), 0, (256));
    n = read(sockfd,buffer,255);
    if (n < 0) 
        error("ERROR reading from socket");
    printf("Ans: %s\n", buffer);
    ans = strtol(buffer, (char **)NULL, 10);
    printf("Ans: %d\n",ans);
    return ans;
}
