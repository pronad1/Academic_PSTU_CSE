#include <iostream>
#include <thread>
#include <mutex>

using namespace std;

mutex wrt;      // Writer lock
mutex mtx;      // Protect readCount

int readCount = 0;
int sharedData = 0;

// Reader Function
void reader(int id)
{
    mtx.lock();
    readCount++;

    // First reader blocks writer
    if (readCount == 1)
        wrt.lock();

    mtx.unlock();

    cout << "Reader " << id << " is reading. Data = "
         << sharedData << endl;

    mtx.lock();
    readCount--;

    // Last reader allows writer
    if (readCount == 0)
        wrt.unlock();

    mtx.unlock();
}

// Writer Function
void writer(int id)
{
    wrt.lock();

    sharedData++;
    cout << "Writer " << id << " is writing. Data = "
         << sharedData << endl;

    wrt.unlock();
}

int main()
{
    thread r1(reader, 1);
    thread r2(reader, 2);
    thread w1(writer, 1);
    thread r3(reader, 3);
    thread w2(writer, 2);

    r1.join();
    r2.join();
    w1.join();
    r3.join();
    w2.join();

    return 0;
}