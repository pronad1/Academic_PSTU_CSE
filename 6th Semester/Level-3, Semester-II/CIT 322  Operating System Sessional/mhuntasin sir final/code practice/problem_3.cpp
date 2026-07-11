#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>

using namespace std;

mutex m;

void write_log(int i)
{
    // acquire lock (efficient waiting)
    unique_lock<mutex> lock(m);

    cout << "Thread " << i << " is writing log..." << endl;

    this_thread::sleep_for(chrono::milliseconds(100));

    cout << "Thread " << i << " finished writing" << endl;

    // lock automatically released when goes out of scope
}

int main()
{
    vector<thread> threads;

    for (int i = 0; i < 5; i++)
    {
        threads.push_back(thread(write_log, i));
    }

    for (auto &t : threads)
    {
        t.join();
    }

    return 0;
}