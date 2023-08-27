#include <bits/stdc++.h>
using namespace std;
// WA

const long long INF = 100000000000000; 
vector<int> visited;
long long solve_recursive(int u, long long tp_cost, const vector<vector<int>> &AL, const vector<int> &L) {
    if (visited[u] > 10) {
        return INF;
    } else {
        visited[u]++;
        if (AL[u].size() == 1) {
            return -L[u];
        } else {
            long long best_cost = INF;
            for (int v : AL[u]) {
                if (L[u] < tp_cost) { // buy
                    best_cost = min(best_cost, solve_recursive(v, L[u], AL, L) + L[u] + 1);
                } else { // don't buy
                    best_cost = min(best_cost, solve_recursive(v, tp_cost, AL, L) + tp_cost);
                }
            }
            return best_cost;
        }
    }
}

long long solve(int i, int N, const vector<vector<int>> &AL, const vector<int> &L) {
    visited.assign(N, 0);
    return solve_recursive(i, INF, AL, L);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    int N; cin >> N;
    vector<int> L(N, -1);
    for (int n = 0; n < N; ++n) {
        cin >> L[n];
    }
    vector<vector<int>> AL(N, vector<int>());
    for (int n = 0; n < N - 1; ++n) {
        int u, v;
        cin >> u >> v;
        u--; v--;
        AL[u].push_back(v);
        AL[v].push_back(u);
    }   

    for (int i = 0; i < N - 1; ++i) {
        cout << solve(i, N, AL, L) << " ";
    } 
    cout << solve(N - 1, N, AL, L) << endl;

    return 0;
}