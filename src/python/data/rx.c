#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
    int fd;
    int baudrate = B230400;
    const char *path = "/dev/ttyAMA0";

    if (argc >= 2) {
	if (!strcmp(argv[1], "-h") || !strcmp(argv[1], "--help")) {
	    fprintf(stderr, "Usage: %s [%s] [%d]\n", argv[0], path, baudrate);
	    return EXIT_SUCCESS;
	} else {
	    path = argv[1];
	    if (argc >=3)
		baudrate = atoi(argv[2]);
	}
    }

    // serial opening
    fprintf(stderr, "Open serial %s\n", path);
    fd = open(path, O_RDONLY | O_NOCTTY);
    if (fd < 0) {
	fprintf(stderr, "Cannot open serial %s: %m\n", path);
	return EXIT_FAILURE;
    }

    // configure serial port
    struct termios  config;
    if(!isatty(fd)) {
	fprintf(stderr,"ERROR: Not a tty\n");
	return EXIT_FAILURE;
    }
    if(tcgetattr(fd, &config) < 0) {
	fprintf(stderr,"ERROR: Can't get configuration of the tty\n");
	return EXIT_FAILURE;
    }
    config.c_iflag &= ~(IGNBRK | BRKINT | ICRNL |
			INLCR | PARMRK | INPCK | ISTRIP | IXON);
    config.c_oflag = 0;
    config.c_lflag &= ~(ECHO | ECHONL | ICANON | IEXTEN | ISIG);
    config.c_cflag &= ~(CSIZE | PARENB);
    config.c_cflag |= CS8;
    config.c_cc[VMIN]  = 1;
    config.c_cc[VTIME] = 0;
    if(cfsetispeed(&config, baudrate) < 0 || cfsetospeed(&config, baudrate) < 0) {
	fprintf(stderr,"ERROR: Can't set baudrate\n");
	return EXIT_FAILURE;
    }
    if(tcsetattr(fd, TCSAFLUSH, &config) < 0) {
	fprintf(stderr,"ERROR: Can't apply new configuration\n");
	return EXIT_FAILURE;
    }

    // opening out file
    int out = open("out", O_WRONLY | O_CREAT | S_IRUSR | S_IWUSR);
    if (out < 0) {
	fprintf(stderr, "Cannot open file out\n");
	return EXIT_FAILURE;
    }

    //writing to the output file
    char rx_buffer[256];
    while(1){
	int rx_length = read(fd, rx_buffer, 256);
	write(out, rx_buffer, rx_length);
    }
    
}
