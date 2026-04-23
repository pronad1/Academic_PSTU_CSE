
#include <iostream>
#include <thread>

using namespace std;

int available_seats = 1; 

bool compare_and_swap(int *addr, int expected, int new_value) {
    if (*addr == expected) {
        *addr = new_value;
        return true;
    }
    return false;
}

void bookSeat(string user) {
    int expected = 1;

    if (compare_and_swap(&available_seats, expected, 0)) {
        cout << user << "successfully booked the seat.\n";
    } else {
        cout << user << " failed to book the seat.\n";
    }
}

int main() {
    thread t1(bookSeat, "User 1");
    thread t2(bookSeat, "User 2");

    t2.join();
    t1.join();

    return 0;
}
