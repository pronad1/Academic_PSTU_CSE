#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <mutex>
#include <condition_variable>

using namespace std;

// ফিলোসফারের ৩টি অবস্থা
enum State { THINKING, HUNGRY, EATING };

// DiningPhilosophers Monitor Class
class DiningPhilosophersMonitor {
private:
    State state[5];             // ৫ জন ফিলোসফারের স্টেট
    condition_variable self[5]; // প্রতি ফিলোসফারের জন্য আলাদা কন্ডিশন ভ্যারিয়েবল
    mutex monitor_mutex;        // মনিটরের ভেতরে একসাথে ১টির বেশি থ্রেড ঢুকতে না দেওয়ার জন্য লক

    // টেস্ট ফাংশন: বাম ও ডান পাশের মানুষ খাচ্ছে কিনা চেক করে
    void test(int id) {
        // যদি নিজে ক্ষুধার্ত হয় এবং পাশের দুজনই EATING অবস্থায় না থাকে
        if (state[id] == HUNGRY && 
            state[(id + 4) % 5] != EATING && 
            state[(id + 1) % 5] != EATING) {
            
            state[id] = EATING; // অবস্থা পরিবর্তন করে EATING করা হলো
            self[id].notify_one(); // ফিলোসফারকে ঘুম থেকে জাগিয়ে দেওয়া (Signal)
        }
    }

public:
    DiningPhilosophersMonitor() {
        for (int i = 0; i < 5; i++) {
            state[i] = THINKING;
        }
    }

    // চামচ তোলার ফাংশن (Pick up chopsticks)
    void pickup(int id) {
        unique_lock<mutex> lock(monitor_mutex); // মনিটরে এন্ট্রি লক
        
        state[id] = HUNGRY;
        cout << "Philosopher " << id << " is HUNGRY.\n";
        
        test(id); // খাওয়া শুরু করা সম্ভব কিনা চেক করো

        // যদি টেস্ট সফল না হয় এবং স্টেট EATING না হয়, তবে অপেক্ষা করো (Wait)
        while (state[id] != EATING) {
            self[id].wait(lock);
        }
    }

    // চামচ নামিয়ে রাখার ফাংশন (Put down chopsticks)
    void putdown(int id) {
        unique_lock<mutex> lock(monitor_mutex); // মনিটরে এন্ট্রি লক

        state[id] = THINKING;
        cout << "Philosopher " << id << " is THINKING.\n";

        // খাওয়া শেষ করে পাশের দুজনকে সুযোগ দেওয়ার জন্য টেস্ট কল করা
        test((id + 4) % 5); // বাম পাশের ফিলোসফারের জন্য চেক
        test((id + 1) % 5); // ডান পাশের ফিলোসফারের জন্য চেক
    }
};

// গ্লোবাল মনিটর অবজেক্ট
DiningPhilosophersMonitor monitor_obj;
mutex cout_mutex; // শুধু কনসোল প্রিন্ট সুন্দর রাখার জন্য

void philosopher(int id) {
    while (true) {
        // ১. থিংকিং স্টেট (মনিটরের বাইরে)
        this_thread::sleep_for(chrono::milliseconds(1000));

        // ২. চামচ তোলার অনুরোধ (মনিটরের ভেতর প্রবেশ)
        monitor_obj.pickup(id);

        // ৩. ক্রিটিক্যাল সেকশন: ফিলোসফার খাচ্ছে
        {
            lock_guard<mutex> lock(cout_mutex);
            cout << "Philosopher " << id << " is EATING ----------->>>>>\n";
        }
        this_thread::sleep_for(chrono::milliseconds(1500));

        // ৪. চামচ নামিয়ে রাখার অনুরোধ (মনিটরের ভেতর প্রবেশ)
        monitor_obj.putdown(id);
    }
}

int main() {
    vector<thread> philosophers;

    for (int i = 0; i < 5; i++) {
        philosophers.emplace_back(philosopher, i);
    }

    for (auto &t : philosophers) {
        t.join();
    }

    return 0;
}