#include <iostream>
using namespace std;

int main() {

    int n = 5; // processes
    int m = 3; // resources

    // Allocation matrix
    int alloc[5][3] = {
        {0, 1, 0},
        {2, 0, 0},
        {3, 0, 2},
        {2, 1, 1},
        {0, 0, 2}
    };

    // Max matrix
    int max[5][3] = {
        {7, 5, 3},
        {3, 2, 2},
        {9, 0, 2},
        {2, 2, 2},
        {4, 3, 3}
    };

    // Available resources
    int avail[3] = {3, 3, 2};

    int finish[5] = {0};
    int safeSeq[5];

    int need[5][3];

    // Calculate NEED matrix
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            need[i][j] = max[i][j] - alloc[i][j];
        }
    }

    int count = 0;

    while (count < n) {
        bool found = false;

        for (int p = 0; p < n; p++) {

            if (!finish[p]) {
                int j;

                for (j = 0; j < m; j++) {
                    if (need[p][j] > avail[j])
                        break;
                }

                if (j == m) {
                    for (int k = 0; k < m; k++) {
                        avail[k] += alloc[p][k];
                    }

                    safeSeq[count++] = p;
                    finish[p] = 1;
                    found = true;
                }
            }
        }

        if (!found) {
            cout << "System is NOT in safe state\n";
            return 0;
        }
    }

    cout << "System is in SAFE state\nSafe sequence: ";

    for (int i = 0; i < n; i++) {
        cout << "P" << safeSeq[i] << " ";
    }

    cout << endl;

    return 0;
}