#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <atomic> 

using namespace std;

// Shared variables
int next_id = 1;
atomic<int> lock_var(0); // থিওরির 'lock' ভ্যারিয়েবল

// Atomic Compare and Swap Function
int compare_and_swap(atomic<int> *value, int expected, int new_value)
{
    int temp = value->load(); // int temp = *value;
    
    // C++ এ compare_exchange_strong এর প্রথম প্যারামিটারটি reference হিসেবে যায় 
    // এবং সেটি পরিবর্তিত হয়ে যায়। তাই থিওরির 'expected' কে ফিক্সড রাখতে 
    // আমরা একটি লোকাল ভ্যারিয়েবল 'exp' ব্যবহার করছি।
    int exp = expected; 
    value->compare_exchange_strong(exp, new_value);
    
    return temp; 
}

// Critical section execution
void generate_id(int i)
{
    // Acquire Lock (while (compare_and_swap(&lock, 0, 1) != 0);)
    while (compare_and_swap(&lock_var, 0, 1) != 0)
    {
        // busy waiting
    }

    /* ------- START OF CRITICAL SECTION ------- */
    int temp = next_id;
    this_thread::sleep_for(chrono::milliseconds(10));
    next_id = temp + 1;

    cout << "Thread " << i << " Assigned ID: " << temp << "\n";
    /* -------- END OF CRITICAL SECTION -------- */

    // Release Lock (lock = 0)
    lock_var.store(0); 
}

int main()
{
    vector<thread> threads;

    for (int i = 0; i < 10; i++)
    {
        threads.emplace_back(generate_id, i);
    }

    for (auto &t : threads)
    {
        t.join();
    }

    return 0;
}