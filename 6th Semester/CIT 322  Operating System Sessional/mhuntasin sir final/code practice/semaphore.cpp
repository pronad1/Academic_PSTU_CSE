#include <iostream>
#include <vector>
#include <chrono>

using namespace std;

// semaphore variable (একদম সাধারণ গ্লোবাল ভ্যারিয়েবল)
int S = 1;   // binary semaphore (1 = available, 0 = locked)

// wait() function (তোমার দেওয়া একদম পিওর থিওরিটিক্যাল স্ট্রাকচার)
void wait(int &S) {
    while (S <= 0) {
        // busy wait (সিঙ্গেল থ্রেডে এখানে আটকাবে না, কারণ S এর মান ১)
    }
    S--;
}

// signal() function (একদম পিওর থিওরিটিক্যাল স্ট্রাকচার)
void signal(int &S) {
    S++;
}

// shared variable
int next_id = 1;

// critical section
void generate_id(int i) {

    wait(S);   // enter critical section (S কমে ০ হবে)

    int temp = next_id;
    next_id = temp + 1;

    // সিঙ্গেল থ্রেড হওয়ায় আউটপুট একদম সিরিয়ালি এবং সুন্দরভাবে আসবে
    cout << "Thread " << i << " Assigned ID: " << temp << endl;

    signal(S); // exit critical section (S বেড়ে আবার ১ হবে)
}

int main() {

    // এখানে কোনো thread অবজেক্ট তৈরি করা হয়নি। 
    // মেইন থ্রেড নিজেই লুপ চালিয়ে একা একা ফাংশনটি ১০ বার কল করবে।
    for (int i = 0; i < 10; i++) {
        generate_id(i);
    }

    return 0;
}