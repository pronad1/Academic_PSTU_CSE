#include <iostream>
#include <thread>
#include <vector>
#include <atomic>

using namespace std;

atomic<int> counter(0);

// increment using CAS
void increment(int id) {
    while (true) {
        int old_value = counter.load();   // expected value
        int new_value = old_value + 1;

        // CAS operation
        if (counter.compare_exchange_weak(old_value, new_value)) {
            cout << "Thread " << id << " updated counter to " << new_value << endl;
            break;
        }
        // else retry automatically
    }
}

int main() {
    vector<thread> threads;

    for (int i = 0; i < 10; i++) {
        threads.push_back(thread(increment, i));
    }

    for (auto &t : threads) {
        t.join();
    }

    cout << "\nFinal Counter: " << counter << endl;

    return 0;
}