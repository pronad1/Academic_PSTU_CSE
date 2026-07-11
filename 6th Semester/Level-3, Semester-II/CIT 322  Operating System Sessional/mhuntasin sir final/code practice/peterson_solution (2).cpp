#include <iostream>
#include <thread>
#include <chrono>

using namespace std;

int next_id = 1;


bool flag[2] = {false, false};
int turn = 0;


void peterson_enter(int i, int j) {
    flag[i] = true;
    turn = j;

    while (flag[j] && turn == j) {
        
    }
}


void peterson_exit(int i) {
    flag[i] = false;
}

void generate_id(int i) {
    int j = 1 - i;

    peterson_enter(i, j);

    int temp = next_id;
    this_thread::sleep_for(chrono::milliseconds(10));
    next_id = temp + 1;

    cout << "Thread " << i << " Assigned ID: " << temp << endl;

    peterson_exit(i);
}

int main() {
    thread t1(generate_id, 0);
    thread t2(generate_id, 1);

    t1.join();
    t2.join();

    return 0;
}