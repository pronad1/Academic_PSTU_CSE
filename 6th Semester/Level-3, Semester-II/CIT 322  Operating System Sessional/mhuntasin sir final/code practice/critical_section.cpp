#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>

using namespace std;

int next_id = 1;
mutex mtx;

void generate_id() {
    mtx.lock();   

    int temp = next_id;
    this_thread::sleep_for(chrono::milliseconds(10)); 
    next_id = temp + 1;

    cout << "Assigned ID: " << temp << endl;

    mtx.unlock();
}

int main() {
    vector<thread> threads;

    for (int i = 0; i < 10; i++) {
        threads.push_back(thread(generate_id));
    }

    for (auto &t : threads) {
        t.join();
    }

    return 0;
}