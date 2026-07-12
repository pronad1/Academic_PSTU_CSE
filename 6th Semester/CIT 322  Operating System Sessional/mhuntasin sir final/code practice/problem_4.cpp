#include <iostream>
#include <thread>
#include <vector>
#include <atomic>

using namespace std;

int balance = 1000;              // shared variable
atomic<bool> lock_var(false);   // lock

bool test_and_set() {
    return lock_var.exchange(true);
}

void acquire_lock() {
    while (test_and_set()) {
        // busy wait
    }
}

void release_lock() {
    lock_var.store(false);
}

void transaction(int id, int amount) {
    acquire_lock();

    // critical section
    if (amount < 0 && balance + amount < 0) {
        cout << "Thread " << id << " Withdrawal failed (Insufficient balance)\n";
    } else {
        balance += amount;
        cout << "Thread " << id << " Updated balance: " << balance << endl;
    }

    release_lock();
}

int main() {
    vector<thread> threads;

    // +ve = deposit, -ve = withdraw
    threads.push_back(thread(transaction, 1, -200));
    threads.push_back(thread(transaction, 2, -500));
    threads.push_back(thread(transaction, 3, 300));
    threads.push_back(thread(transaction, 4, -700));
    threads.push_back(thread(transaction, 5, 200));

    for (auto &t : threads) {
        t.join();
    }

    cout << "\nFinal Balance: " << balance << endl;

    return 0;
}