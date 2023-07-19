#include <bits/stdc++.h>
using namespace std;

int main() {
    const long long p = 2272978429;
    // const int g = 2;
    const long long A = 1116819144;

    long long ans = 1;
    for (long long b = 1; b < p; ++b) {
        ans *= 2;
        ans %= p;
        if (ans == 1042188408) {
            cout << b << endl;
        }
    }

    return 0;
}
