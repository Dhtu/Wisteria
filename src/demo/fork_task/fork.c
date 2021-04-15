
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>  // 系统调用的封装
#include<sys/wait.h>  //wait/waitpid时使用

int main()
{
	int i;
	printf("父进程！ pid=%d\n", getpid());
	pid_t p1id = fork();  //如果fork成功，会向父进程返回子进程的id,并向子进程0
	printf("第一次%d\n", (int)p1id);
	if (p1id < 0)
	{
		printf("fork创建子进程1失败！\n");
		return 0;
	}
	else if (p1id == 0)
	{
		for (i = 0; i < 3; i++)
			printf("这是子进程1，id为：%d，它的父进程id为：%d\n", (int)getpid(), (int)getppid());
		exit(0);
	}

	//创建第二个进程
	pid_t p2id = fork();
	printf("第二次%d\n", (int)p2id);
	if (p2id < 0)
	{
		printf("fork创建子进程2失败！\n");
		exit(0);
	}
	else if (p2id == 0)
	{
		for (i = 0; i < 3; i++)
		{
			printf("这是子进程2，id为：%d,它的父进程id为：%d\n", (int)getpid(), (int)getppid());
		}
		exit(0);
	}

	waitpid(p1id, NULL, 0);
	waitpid(p2id, NULL, 0);
	printf("这是父进程退出，父进程id为：%d\n", getpid());
	return 0;
}
