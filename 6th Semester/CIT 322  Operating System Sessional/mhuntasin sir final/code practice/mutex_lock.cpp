#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <atomic> // atomic ব্যবহার করতে হবে যেন check এবং write ইন্টারাপ্ট না হয়

using namespace std;

// shared variables
// ordinary bool এর জায়গায় atomic<bool> ব্যবহার করা হয়েছে
atomic<bool> available(true); 
int next_id = 1;

// acquire function (ঠিক তোমার স্ট্রাকচার অনুযায়ী)
void acquire() {
    // while (!available) ; available = false;
    // এখানে exchange(false) একবারে চেক করে এবং false সেট করে (Atomically)
    while (!available.exchange(false)) {
        // busy wait
    }
}

// release function (ঠিক তোমার স্ট্রাকচার অনুযায়ী)
void release() {
    available = true;
}

// critical section
void generate_id(int i) {

    acquire();   // lock

    int temp = next_id;
    this_thread::sleep_for(chrono::milliseconds(10));
    next_id = temp + 1;

    // Output গিজমিজ হওয়া বন্ধ করতে এবং সিরিয়াল ঠিক রাখতে 
    cout << "Thread " << i << " Assigned ID: " << temp << "\n";

    release();   // unlock
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