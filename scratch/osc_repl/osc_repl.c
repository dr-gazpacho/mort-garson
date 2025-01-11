#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SC_PORT 57120
#define BUFFER_SIZE 1024

int send_osc_message(const char *path, const char *name, int freq) {
    int sockfd;
    struct sockaddr_in servaddr;
    char buffer[BUFFER_SIZE];
    int size;
    
    // Create socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Socket creation failed");
        return -1;
    }
    
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(SC_PORT);
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    
    // Basic OSC message formatting
    size = sprintf(buffer, "%s,%s,%d", path, name, freq);
    
    sendto(sockfd, buffer, size, 0,
           (struct sockaddr *)&servaddr, sizeof(servaddr));
    
    close(sockfd);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage:\n");
        printf("  create synth: %s create <name> <freq>\n", argv[0]);
        printf("  change freq: %s freq <name> <freq>\n", argv[0]);
        printf("  free synth: %s free <name>\n", argv[0]);
        printf("  free all: %s freeall\n", argv[0]);
        return 1;
    }

    const char *command = argv[1];

    if (strcmp(command, "create") == 0) {
        if (argc != 4) return 1;
        send_osc_message("/synth/create", argv[2], atoi(argv[3]));
    }
    else if (strcmp(command, "freq") == 0) {
        if (argc != 4) return 1;
        send_osc_message("/synth/params", argv[2], atoi(argv[3]));
    }
    else if (strcmp(command, "free") == 0) {
        if (argc != 3) return 1;
        send_osc_message("/synth/free", argv[2], 0);
    }
    else if (strcmp(command, "freeall") == 0) {
        send_osc_message("/synth/freeAll", "", 0);
    }

    return 0;
}