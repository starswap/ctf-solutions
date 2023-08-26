#include <bits/stdc++.h>
using namespace std;

// SEKAI{hyp3rL1nk_cha115_4r3_EZ}

const int INF = 1000000;

bool bfs_check(int s, int t, const vector<vector<int>> &AL, int V) {
    queue<pair<int, int>> q;
    vector<int> costs(V, INF);
    q.emplace(s, 0);
    costs[s] = 0;
    while (q.size() > 0) {
        auto [u, d] = q.front(); q.pop();
        for (int v : AL[u]) {
            if (costs[v] == INF) {
                costs[v] = d + 1;
                q.emplace(v, d + 1);
            }
        }
    } 
    return costs[t] <= 6;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    int T; cin >> T;
    for (int t = 0; t < T; ++t) {
        int V, E;
        cin >> V >> E;
        vector<vector<int>> AL(V, vector<int>());
        for (int e = 0; e < E; ++e) {
            int u, v;
            cin >> u >> v;
            AL[u].push_back(v);
            // AL[v].push_back(u);
        }
        int s, targ;
        cin >> s >> targ;
        cout << ((bfs_check(s, targ, AL, V) ? "YES" : "NO")) << endl;
    }
    return 0;
}