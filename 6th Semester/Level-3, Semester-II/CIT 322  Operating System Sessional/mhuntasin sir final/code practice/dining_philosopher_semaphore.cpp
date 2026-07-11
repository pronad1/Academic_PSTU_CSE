#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <semaphore> // C++20 এর স্ট্যান্ডার্ড সেমাফোর হেডার
#include <mutex>

using namespace std;

// ৫টি চামচের জন্য ৫টি বাইনারি সেমাফোর (১ মানে ফাঁকা, ০ মানে লক)
// counting_semaphore<1> মূলত একটি বাইনারি সেমাফোর হিসেবে কাজ করে
binary_semaphore chopstick[5]{
    binary_semaphore{1}, binary_semaphore{1}, binary_semaphore{1}, 
    binary_semaphore{1}, binary_semaphore{1}
};

// টেবিলে একসাথে সর্বোচ্চ ৪ জন বসতে পারবে (Counting Semaphore)
counting_semaphore<5> room(4); 

mutex cout_mutex; // আউটপুট টেক্সট সুন্দরভাবে প্রিন্ট করার জন্য

void philosopher(int id) {
    while (true) {
        // ১. ফিলোসফার চিন্তা করছে
        {
            lock_guard<mutex> lock(cout_mutex);
            cout << "Philosopher " << id << " is THINKING.\n";
        }
        this_thread::sleep_for(chrono::milliseconds(1000));

        // ২. ডাইনিং রুমে ঢোকার পারমিশন নেওয়া (wait/acquire)
        room.acquire(); 

        // ৩. বাম পাশের চামচ নেওয়া (wait/acquire)
        chopstick[id].acquire();
        
        // ৪. ডান পাশের চামচ নেওয়া (wait/acquire)
        chopstick[(id + 1) % 5].acquire();

        // ৫. ফিলোসফার খাচ্ছে (Critical Section)
        {
            lock_guard<mutex> lock(cout_mutex);
            cout << "Philosopher " << id << " is EATING ----------->>>>>\n";
        }
        this_thread::sleep_for(chrono::milliseconds(1500));

        // ৬. ডান পাশের চামচ রেখে দেওয়া (signal/release)
        chopstick[(id + 1) % 5].release();
        
        // ৭. বাম পাশের চামচ রেখে দেওয়া (signal/release)
        chopstick[id].release();

        // ৮. ডাইনিং রুম থেকে বের হয়ে যাওয়া (signal/release)
        room.release(); 
    }
}

int main() {
    vector<thread> philosophers;

    // ৫ জন ফিলোসফারের জন্য ৫টি থ্রেড তৈরি করা হচ্ছে
    for (int i = 0; i < 5; i++) {
        philosophers.emplace_back(philosopher, i);
    }

    // থ্রেডগুলো আজীবন চলতে থাকবে
    for (auto &t : philosophers) {
        t.join();
    }

    return 0;
}