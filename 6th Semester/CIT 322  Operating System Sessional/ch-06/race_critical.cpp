#include <iostream>
#include <thread>
#include <vector>
#include <chrono>

using namespace std;

int next_id = 1000;

void process_admission(int student_index)
{
    int assigned_id = next_id;

    this_thread::sleep_for(chrono::milliseconds(5));

    next_id = assigned_id + 1;

    cout << "Student " << student_index << " received ID: " << assigned_id << "\n";
}

int main()
{
    int num_students = 10;
    vector<thread> admission_threads;

    cout << "Processing " << num_students << " admission requests (Without Synchronization)...\n\n";

    for (int i = 1; i <= num_students; ++i)
    {
        admission_threads.push_back(thread(process_admission, i));
    }

    for (auto &t : admission_threads)
    {
        t.join();
    }

    cout << "\n--- Final Result ---\n";
    cout << "Expected Next ID to be: " << 1000 + num_students << "\n";
    cout << "Actual Next ID is     : " << next_id << "\n";

    if (next_id != 1000 + num_students)
    {
        cout << "CRITICAL ISSUE: Duplicate IDs assigned because of race condition!\n";
    }
    else
    {
        cout << "SUCCESS: Processed successfully (rare without synchronization!).\n";
    }

    return 0;
}