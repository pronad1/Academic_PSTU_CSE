#include <iostream>
#include <thread>
#include <queue>
#include <mutex>
#include <condition_variable>

using namespace std;

const int MAX_SIZE = 5;

queue<int> buffer;
mutex mtx;
condition_variable cv;

void producer(int id) {
    for (int i = 0; i < 10; i++) {

        unique_lock<mutex> lock(mtx);

        while (buffer.size() == MAX_SIZE) {
            cv.wait(lock);   // wait if buffer is full
        }

        buffer.push(i);
        cout << "Producer " << id << " produced " << i << endl;

        cv.notify_all();
    }
}

void consumer(int id) {
    for (int i = 0; i < 10; i++) {

        unique_lock<mutex> lock(mtx);

        while (buffer.empty()) {
            cv.wait(lock);   // wait if buffer is empty
        }

        int item = buffer.front();
        buffer.pop();

        cout << "Consumer " << id << " consumed " << item << endl;

        cv.notify_all();
    }
}

int main() {
    thread p1(producer, 1);
    thread c1(consumer, 1);

    p1.join();
    c1.join();

    return 0;
}