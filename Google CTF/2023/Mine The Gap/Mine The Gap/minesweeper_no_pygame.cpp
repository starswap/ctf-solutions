#include <bits/stdc++.h>
using namespace std;

const int GRID_HEIGHT = 1632;
const int GRID_WIDTH = 3600;

const int dr[] = {-1,1,0,0,1,1,-1,-1};
const int dc[] = {0,0,1,-1,1,-1,-1,1};

char grid[GRID_HEIGHT][GRID_WIDTH];
bool visited[GRID_HEIGHT][GRID_WIDTH] = {};

void readin() {
    string curr_line;
    ifstream gameboard("gameboard.txt");

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

bool too_few(int r, int c, int oldr, int oldc) {
    int newr; int newc;
    if (grid[r][c] >= '1' && grid[r][c] <= '8') {
        int count = 0;
        for (int i = 0; i < 8; ++i) { // go through all neighbours
            newr = r + dr[i];
            newc = c + dc[i];
            if (!((newc == oldc && newr > oldr) || newc  > oldc) && grid[newr][newc] == '9') // require that it's not the same one, and also that it comes after
                continue;
            if (grid[newr][newc] == '9' || grid[newr][newc] == 'A' || grid[newr][newc] == 'B') // max mines = all 9 plus 10 and 11
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
    int nextr; int nextc;

    while (r < GRID_HEIGHT - 1 && grid[r][c] == ' ') {
        r++;
    }
    if (grid[r][c] == ' ') {
        return solve(0, c + 1);
    }

    if (maxi == 3503) {
        cout << r << ", " << c << endl;
    }
    if (c > maxi) { //  tracking
       cout << c << endl;
        maxi = c;
    }
    maxir = max(r, maxir);
    if (c  == 3503 && r == 62) {
        cout << r << endl;
//        return true;
    }
//    if (maxi == 3503) {
    //    cout << r << " " << c << endl;
  //  }
    
    if (r == GRID_HEIGHT -1 and c == GRID_WIDTH - 1)
        return 1;

    if (r < GRID_HEIGHT - 1) {
        nextr = r + 1;
        nextc = c;
    }
    else {
        nextr = 0;
        nextc = c + 1;
    }

    if (grid[r][c] == '9') {
        grid[r][c] = 'A';
        bool ok = 1;
        for (int i = 0; i < 8; ++i) {
            if (too_many(r + dr[i], c + dc[i])) {
                ok = 0; 
                break;
            }
        }

        if (!ok || !solve(nextr, nextc)) {// try not flagging
            grid[r][c] = '9'; // turn this one off
            ok = 1;
            for (int i = 0; i < 8; ++i) {
                if (too_few(r + dr[i], c + dc[i], r, c)) {
                    ok = 0; 
                    break;
                }
            } 

            if (!ok) { 
                if (c == 3503 && r == 62) {
//                    cout << "Case 1" << endl;
                }
                return 0;
            }
            else {
                if (c == 3503 && r == 62) {
                    cout << "Case 2" << endl;
                }
                return solve(nextr, nextc);
            }
        }
        else {
            return 1;
        }
    }
    else {
        if (c == 3503 && r == 62) {
            cout << "Case 3" << endl;
        }
        return solve(nextr, nextc);
    }
}




int main () {
    readin();
    cout << "Success was: " << solve(0,0) << endl;
    cout << "Outting" << endl;
    writeout();    
}

