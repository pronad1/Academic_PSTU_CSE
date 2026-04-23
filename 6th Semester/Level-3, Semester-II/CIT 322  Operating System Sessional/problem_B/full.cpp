#include <bits/stdc++.h>
#include <sys/wait.h>
using namespace std;

int main()
{
    int pid = fork();

    if (pid < 0)
    {
        cout << "Error in fork()" << endl;
    }
    else if (pid == 0)
    {
        cout << "Child process with PID: " << getpid() << endl;
        execlp("ls", "ls", "-l", NULL);
    }
    else
    {
        cout << "Parent process with PID: " << getpid() << endl;
        wait(NULL);
    }
}