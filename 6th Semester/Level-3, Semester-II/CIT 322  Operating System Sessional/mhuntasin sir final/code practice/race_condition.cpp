#include<bits/stdc++.h>
using namespace std::chrono;
using namespace std;
int next_id = 1;

void generate_id() {
    int temp = next_id;
    this_thread::sleep_for(milliseconds(10));
    next_id = temp + 1;

    cout << "Assigned ID: " << temp << endl;
}

int main() {
    vector<thread> threads;

    for (int i = 0; i < 10; i++) {
        threads.push_back(thread(generate_id));
    }

    for (auto &t : threads) {
        t.join();
    }

    return 0;
}