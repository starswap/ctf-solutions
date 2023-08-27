import json
from websockets.sync.client import connect
from collections import deque
import heapq

SOCK_URL = "ws://mikusweeper.chals.sekai.team/socket"
DISP = {
    "covered": "#",
    "c0": " ",
    "c1": "1",
    "c2": "2",
    "c3": "3",
    "c4": "4",
    "c5": "5",
    "c6": "6",
    "c7": "7",
    "c8": "8",
    "bomb": "B",
    "safe": "S",
    "key": "K",
}
R = 0
C = 0

dr = [0, 0, 1, 1, 1, -1, -1, -1]
dc = [1, -1, 0, 1, -1, 0, 1, -1]

MOVES = ["right", "left", "up", "down"]
dr_m = [0, 0, -1, 1]
dc_m = [1, -1, 0, 0]

def is_number(sq):
    return sq[0] == 'c' and sq[1].isdigit()

def neighbours(r, c):
    for i in range(8):
        yield((dr[i] + r, dc[i] + c))

def movable_neighbours(r, c):
    for i in range(4):
        yield((dr_m[i] + r, dc_m[i] + c, MOVES[i]))

def in_bounds(r, c):
    return r >= 0 and r < R and c >= 0 and c < C

def mark_mines():
    global game_state
    board = game_state["map"]
    for r, row in enumerate(board):
        for c, sq in enumerate(row):
            if is_number(sq):
                num_mines = int(sq[1:])
                num_potential_mines = 0
                
                for new_r, new_c in neighbours(r, c):
                    if (in_bounds(new_r, new_c) and board[new_r][new_c] in ("covered", "bomb")):
                        num_potential_mines += 1
                
                if num_potential_mines == num_mines:
                    for new_r, new_c in neighbours(r, c):
                        if in_bounds(new_r, new_c) and board[new_r][new_c] in ("covered", "bomb"):
                            board[new_r][new_c] = "bomb"
    game_state["map"] = board

def mark_safe():
    global game_state
    board = game_state["map"]
    for r, row in enumerate(board):
        for c, sq in enumerate(row):
            if is_number(sq):
                num_mines = int(sq[1:])
                num_found_mines = 0
                for (new_r, new_c) in neighbours(r, c):
                    if in_bounds(new_r, new_c) and board[new_r][new_c] == "bomb":
                        num_found_mines += 1

                if num_found_mines == num_mines:
                    for (new_r, new_c) in neighbours(r, c):
                        if (in_bounds(new_r, new_c) and board[new_r][new_c] == "covered"):
                            board[new_r][new_c] = "safe"
    board = game_state["map"]

def route_to_square(board, hero_r, hero_c, targ_r, targ_c):
    q = [(abs(targ_r - hero_r) + abs(targ_c - hero_c), hero_r, hero_c, [], 0)]
    # print(targ_r)
    # print(targ_c)
    heapq.heapify(q)
    visited = set([])
    
    while len(q) != 0:
        (heuristic, r, c, moves, n) = heapq.heappop(q)
        if (r, c) == (targ_r, targ_c):
            return moves
        for (new_r, new_c, move) in movable_neighbours(r, c):
            if in_bounds(new_r, new_c) and not (board[new_r][new_c] in ("covered", "bomb")) and not (new_r, new_c) in visited:
                visited.add((new_r,new_c))
                new_heuristic = abs(targ_r - new_r) + abs(targ_c - new_c) + n + 1
                heapq.heappush(q, (new_heuristic, new_r, new_c, moves + [move], n + 1))
    return None

def go_to_type(typeOf):
    global websocket, game_state
    for r, row in enumerate(game_state["map"]):
        for c, sq in enumerate(row):
            if sq == typeOf:
                # print("start")
                route = route_to_square(game_state["map"], game_state["hero"]["y"], game_state["hero"]["x"], r, c)
                # print(route)
                if route is not None:
                    do_steps(route)

def go_to_safe():
    go_to_type("safe")

def go_to_keys():
    go_to_type("key")

def open_squares(board):
    uncovered = 0
    for row in board:
        for sq in row:
            if sq != "covered":
                uncovered += 1
    return uncovered

def do_steps(route):
    global game_state
    websocket.send('\n'.join(route))
    new_state = json.loads(websocket.recv())
    new_state["map"] = merge_board(game_state["map"], new_state["map"])
    game_state = new_state

def do_step(step):
    global game_state
    websocket.send(step)
    new_state = json.loads(websocket.recv())
    new_state["map"] = merge_board(game_state["map"], new_state["map"])
    game_state = new_state
    # print_board()

def status_update():
    print(f"Got {game_state['numKeysRetrieved']} keys with {game_state['livesRemaining']} lives left")
    print("Open squares: " + str(open_squares(game_state["map"])))

game_state = {
    "numKeysRetrieved": 0,
    "livesRemaining": 8,
    "map": [],
    "hero": {"x": 0, "y": 0},
}

def print_board():
    global game_state
    board = game_state["map"]
    heror = game_state["hero"]["y"]
    heroc = game_state["hero"]["x"]
    for r, row in enumerate(board):
        ans = ("".join(map(lambda x: DISP[x], row)))
        if r == heror:
            ans = ans[:heroc] + "H" + ans[heroc + 1:]
        print(ans)
    print("\n")

def merge_board(old_board, new_board):
    for r, row in enumerate(old_board):
        for c, sq in enumerate(row):
            if (sq == 'safe' or sq == 'bomb') and new_board[r][c] == "covered":
                new_board[r][c] = sq
    return new_board 

def play_game():
    global websocket, game_state, R, C

    with connect(SOCK_URL) as websocket:
        message = websocket.recv()

        game_state = json.loads(message)
        R = len(game_state['map'])
        C = len(game_state['map'][0])
        
        while not(game_state["numKeysRetrieved"] == 40):
            old_game_state = game_state
            status_update()
            mark_mines()
            mark_safe()
            go_to_safe()
            go_to_keys()
            if game_state == old_game_state:
                break
        
        print(game_state["flag"])

# merge mines
# sort by distance

# multiprocessing?

play_game()

# random if no options