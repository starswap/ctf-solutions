#include <bits/stdc++.h>
using namespace std;

const int GRID_HEIGHT = 11; // 1632;
const int GRID_WIDTH = 42; // 3600;

const int dr[] = {1,0,-1,0,1,1,-1,-1};
const int dc[] = {0,1,0,-1,1,-1,-1,1};

char grid[GRID_HEIGHT][GRID_WIDTH];
bool visited[GRID_HEIGHT][GRID_WIDTH] = {};

void readin() {
    string curr_line;
    ifstream gameboard("small.txt");

    int r = 0;
    while (getline(gameboard, curr_line)) {
        int col = 0;
        for (char c : curr_line) {		
            grid[r][col] = c;
            col++;
        }
        r++;
    }

    // Close the file
    gameboard.close();
}

void writeout() {
    ofstream outfile("output.txt");
    for (int r = 0; r < GRID_HEIGHT; ++r) {
        string outline = "";
        for (int c = 0; c < GRID_WIDTH; ++c) {
            outline += grid[r][c];
        } 
        outfile << outline << '\n';
    }
    outfile.close();
}

bool too_many(int r, int c) {
    int newr; int newc;
    if (grid[r][c] >= '1' and grid[r][c] <= '8') {
        int count = 0;
        for (int i=0; i < 8; ++i) { // go through all neighbours
            newr = r + dr[i];
            newc = c + dc[i];
            if (grid[newr][newc] == 'A' || grid[newr][newc] == 'B') { 
                count += 1;
            }
        }
        return count > (grid[r][c] - '0');
    }
    else {
        return 0;
    }
}

bool too_few(int r, int c) {
    int newr; int newc;
    if (grid[r][c] >= '1' && grid[r][c] <= '8') {
        int count = 0;
        for (int i = 0; i < 8; ++i) { // go through all neighbours
            newr = r + dr[i];
            newc = c + dc[i];
            if ((!visited[newr][newc] && grid[newr][newc] == '9') || grid[newr][newc] == 'A' || grid[newr][newc] == 'B') // max mines = all 9 plus 10 and 11
                count += 1;
        }
        return count < (grid[r][c] - '0'); 
    } else {
        return 0; 
    }
}

int maxi = 0;
int maxir = 0;
bool solve(int r, int c) {
    bool ok;

//      cout << r << " " << c << endl;
    
    // seen already
    if (visited[r][c] || grid[r][c] == ' ') {
        return true;
    }

    visited[r][c] = true;

    if (grid[r][c] == '9') {
        // set:
        grid[r][c] = 'A';
        ok = true;
        for (int i = 0; i < 8; ++i) {    
            int nextr = r + dr[i];
            int nextc = c + dc[i];
            if (too_many(nextr, nextc)) {
                ok = false;
                break;
            }
        }

        for (int i = 0; i < 8; ++i) {    
            int nextr = r + dr[i];
            int nextc = c + dc[i];
            ok &= solve(nextr, nextc);
        }

        if (ok) {
            return true;
        } else {
            grid[r][c] = '9';
            bool ok = true;
            for (int i = 0; i < 8; ++i) {    
                int nextr = r + dr[i];
                int nextc = c + dc[i];
                if (too_few(nextr, nextc)) {
                    ok = false;
                    break;
                }
            }

            for (int i = 0; i < 8; ++i) {    
                int nextr = r + dr[i];
                int nextc = c + dc[i];
                ok &= solve(nextr, nextc);
            }
            visited[r][c] = false;
            return ok;
        }
    } else {
        ok = true;
        for (int i = 0; i < 8; ++i) {    
            int nextr = r + dr[i];
            int nextc = c + dc[i];
            ok &= solve(nextr, nextc);
        }
        visited[r][c] = false;
        return ok;
    }
}


int main () {
    readin();
    cout << "started with: " << grid[3][9] << endl;
    cout << "Success was: " << solve(3,9) << endl;
    cout << "Outting" << endl;
    writeout();    
}

