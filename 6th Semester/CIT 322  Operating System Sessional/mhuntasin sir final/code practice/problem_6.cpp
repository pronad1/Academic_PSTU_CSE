#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <condition_variable>
#include <chrono>

using namespace std;

mutex mtx;
condition_variable cv;
bool printer_busy = false;

void use_printer(int id) {
    unique_lock<mutex> lock(mtx);

    while (printer_busy) {
        cv.wait(lock);   // no busy waiting
    }

    printer_busy = true;

    cout << "Student " << id << " is printing..." << endl;
    this_thread::sleep_for(chrono::milliseconds(100));

    cout << "Student " << id << " finished printing" << endl;

    printer_busy = false;

    cv.notify_one();
}

int main() {
    vector<thread> students;

    for (int i = 0; i < 5; i++) {
        students.push_back(thread(use_printer, i));
    }

    for (auto &t : students) {
        t.join();
    }

    return 0;
}