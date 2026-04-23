#include <bits/stdc++.h>
using namespace std;

int balance = 0;
bool locker = false;

void acquire_locker() {
    while(locker);
    locker = true;
}

void release_locker() {
    locker = false;
}

void func() {
    acquire_locker();

    int local_bal = balance;
    local_bal++;
    cout << local_bal << endl;
    balance = local_bal;

    release_locker();
}

int main() {
    thread t1(func);
    thread t2(func);

    t1.join();  
    t2.join();  
    cout << "Final bal. -> " << balance << endl;

    return 0;
}