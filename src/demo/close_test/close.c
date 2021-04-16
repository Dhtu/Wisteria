#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<fcntl.h>
#include<unistd.h>
int main()
{
	int fd = open("myfile", O_RDWR|O_CREAT);
	int ret = 0;
	int i = 0;
	if (fd < 0)
	{
		perror("open fail\n");
		exit(1);
	}
	else
		printf("open success\n");
	//const char* msg = "hello this is test_close\n";
	//int count = 10;
	//while (count--)
	//{
	//	write(fd, msg, strlen(msg));
	//}
	//char buf[1024] = { 0 };
	//int num = 10;
	//while (num--)
	//{
	//	read(fd, buf, strlen(msg));
	//}
	for (i = 0; i < 3; ++i)
	{
		if (ret = close(fd) == -1)
			printf("close fail\n");
		else
			printf("close success\n");
	}
	return 0;
}
