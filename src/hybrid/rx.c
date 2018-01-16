#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  int fd;
  int baudrates[13] = {B110,B1200,B2400,B9600,0,B19200,B38400,B57600,0,B115200,B230400,B460800,B921600};
  int baudrate = baudrates[11-1];
  const char *path = "/dev/ttyAMA0";
  
  // argument parsing
  if (argc >= 2) {
    if (!strcmp(argv[1], "-h") || !strcmp(argv[1], "--help")) {
      fprintf(stderr, "Usage: %s baudrate [%d] path [%s]\n", argv[0], baudrate, path);
      fprintf(stderr, "Possibles baudrates : \n\
[1] 110\n\
[2] 1200\n\
[3] 2400\n\
[4] 9600\n\
[5] UNUSED\n\
[6] 19200\n\
[7] 38400\n\
[8] 57600\n\
[9] UNUSED\n\
[10] 115200\n\
[11] 230400\n\
[12] 460800\n\
[13] 921600\n");
      return EXIT_SUCCESS;
    } else {
      int place = atoi(argv[1])-1;
      if (place >= 1 && place <= 13) {
	baudrate = baudrates[place];
	printf("Baudrate set at %d\n", baudrate);
      }
      if (argc >=3) 
	path = argv[2];
      printf("serial path : %s\n", path);
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
  int out = open("out", O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);
  if (out < 0) {
    fprintf(stderr, "Cannot open file out\n");
    return EXIT_FAILURE;
  }

  //writing to the output file
  char rx_buffer[256];
  while(1){
    int rx_length = read(fd, rx_buffer, 256);
    if (rx_buffer[rx_length-1] == '>') {
      rx_length--;
      write(out, rx_buffer, rx_length);
      break;
    }
    write(out, rx_buffer, rx_length);
  }
  
}
