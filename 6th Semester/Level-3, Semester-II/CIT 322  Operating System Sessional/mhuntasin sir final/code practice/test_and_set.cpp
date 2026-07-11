#include <iostream>
#include <thread>
#include <vector>
#include <chrono>

using namespace std;

// Global variables
int next_id = 1;
bool lock_var = false;

// Test and Set
bool test_and_set(bool *target) {
    bool rv = *target;
    *target = true;
    return rv;
}

// Acquire lock
void acquire_lock() {
    while (test_and_set(&lock_var)) {
        // Busy waiting
    }
}

// Release lock
void release_lock() {
    lock_var = false;
}

// Critical section
void generate_id(int i) {
    acquire_lock();

    int temp = next_id;
    this_thread::sleep_for(chrono::milliseconds(10));
    next_id = temp + 1;

    cout << "Thread " << i
         << " Assigned ID: "
         << temp << endl;

    release_lock();
}

int main() {
    vector<thread> threads;

    for (int i = 0; i < 10; i++) {
        threads.emplace_back(generate_id, i);
    }

    for (auto &t : threads) {
        t.join();
    }

    return 0;
}