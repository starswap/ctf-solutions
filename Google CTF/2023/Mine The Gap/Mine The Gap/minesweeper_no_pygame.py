import sys
import itertools
import hashlib
from typing import List, Tuple

# pip install pygame
# import pygame
# from pygame.locals import *

# pygame.init()
 
# FPS = 60
# FramePerSec = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# DISPLAYSURF.fill(WHITE)
# pygame.display.set_caption("Game")

CELL_SIZE = 18

# Images taken from https://hu.wikipedia.org/wiki/Aknakeres%C5%91_(vide%C3%B3j%C3%A1t%C3%A9k)
# Images created by Kazukiokumura and distributed under CC BY-SA 4.0 License
# textures = {
#     'flag': pygame.transform.scale(pygame.image.load("img/flag.png"), (CELL_SIZE, CELL_SIZE)),
#     'cell0': pygame.transform.scale(pygame.image.load("img/cell0.png"), (CELL_SIZE, CELL_SIZE)),
#     'cell1': pygame.transform.scale(pygame.image.load("img/cell1.png"), (CELL_SIZE, CELL_SIZE)),
#     'cell2': pygame.transform.scale(pygame.image.load("img/cell2.png"), (CELL_SIZE, CELL_SIZE)),
#     'cell3': pygame.transform.scale(pygame.image.load("img/cell3.png"), (CELL_SIZE, CELL_SIZE)),
#     'cell4': pygame.transform.scale(pygame.image.load("img/cell4.png"), (CELL_SIZE, CELL_SIZE)),
#     'cell5': pygame.transform.scale(pygame.image.load("img/cell5.png"), (CELL_SIZE, CELL_SIZE)),
#     'cell6': pygame.transform.scale(pygame.image.load("img/cell6.png"), (CELL_SIZE, CELL_SIZE)),
#     'cell7': pygame.transform.scale(pygame.image.load("img/cell7.png"), (CELL_SIZE, CELL_SIZE)),
#     'cell8': pygame.transform.scale(pygame.image.load("img/cell8.png"), (CELL_SIZE, CELL_SIZE)),
#     'closed': pygame.transform.scale(pygame.image.load("img/cell_close.png"), (CELL_SIZE, CELL_SIZE)),
# }

# class QuadTree(object):
#     CAPACITY = 100

#     def __init__(self, rect: pygame.Rect):
#         self.rect = rect
#         self.quads = None
#         self.items = []

#     def add(self, item) -> bool:
#         if not item.rect.colliderect(self.rect):
#             return False
        
#         if len(self.items) < QuadTree.CAPACITY:
#             self.items.append(item)
#             return True

#         if not self.quads:
#             left = self.rect.left
#             top = self.rect.top
#             new_width = self.rect.width/2
#             new_height = self.rect.height/2

#             self.quads = [
#                 QuadTree(pygame.Rect(left, top, new_width, new_height)),
#                 QuadTree(pygame.Rect(left+new_width, top, new_width, new_height)),
#                 QuadTree(pygame.Rect(left, top+new_height, new_width, new_height)),
#                 QuadTree(pygame.Rect(left+new_width, top+new_height, new_width, new_height)),
#             ]

#         if self.quads[0].add(item): return True
#         if self.quads[1].add(item): return True
#         if self.quads[2].add(item): return True
#         if self.quads[3].add(item): return True

#         return False

#     def intersect(self, rect: pygame.Rect) -> List[pygame.sprite.Sprite]:
#         res = []
#         if not self.rect.colliderect(rect):
#             return res

#         for item in self.items:
#             if item.rect.colliderect(rect):
#                 res.append(item)

#         if not self.quads:
#             return res
        
#         for quad in self.quads:
#             res += quad.intersect(rect)
        
#         return res

#     def intersectpoint(self, p: Tuple[int, int]) -> List[pygame.sprite.Sprite]:
#         res = []
#         if not self.rect.collidepoint(p):
#             return res

#         for item in self.items:
#             if item.rect.collidepoint(p):
#                 res.append(item)

#         if not self.quads:
#             return res
        
#         for quad in self.quads:
#             res += quad.intersectpoint(p)
        
#         return res

class Cell():
    def __init__(self, textures, state, x, y):
        super().__init__()
        self.textrues = textures
        # self.rect = textures['cell0'].get_rect()
        # self.rect.center = (CELL_SIZE*x, CELL_SIZE*y)
        self.state = state
        self.update_texture()

    def update(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def draw(self, surface, offset):
        dest = self.rect.move(-offset.left, -offset.top)
        surface.blit(self.image, dest)

    def update_texture(self):
        # if self.state in range(0, 9):
        #     self.image = self.textrues[f'cell{self.state}']
        # elif self.state == 9:
        #     self.image = self.textrues[f'closed']
        # elif self.state == 10: # Chosen mine
        #     self.image = self.textrues[f'flag']
        # elif self.state == 11: # Fixed mine
        #     self.image = self.textrues[f'flag']
        # else:
        #     print(f'Invalid state {self.state}')
        pass

    def click(self):
        if self.state == 9:
            self.state = 10
        elif self.state == 10:
            self.state = 9
        else:
            return
        self.update_texture()

# font = pygame.font.SysFont(None, 24)

cells = []

with open('gameboard.txt', 'r') as fin:
    circuit = fin.read()
    circuit = circuit.replace(' ', '0')
    circuit = [list(line) for line in circuit.split('\n') if len(line) > 0]

GRID_WIDTH = len(circuit[0])
GRID_HEIGHT = len(circuit)

print(GRID_WIDTH)
print(GRID_HEIGHT)

# grid = QuadTree(pygame.Rect(-100, -100, CELL_SIZE*GRID_WIDTH + 100, CELL_SIZE*GRID_HEIGHT + 100))
validate_grid = [[None for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        
for i, (x, y) in enumerate(itertools.product(range(GRID_WIDTH), range(GRID_HEIGHT))):

    # for event in pygame.event.get():              
    #     if event.type == QUIT:
    #         pygame.quit()
    #         sys.exit()

    if i % 100000 == 0:
        print(i)
    #     DISPLAYSURF.fill(WHITE)
    #     progress = (i / (GRID_WIDTH*GRID_HEIGHT))*100
    #     img = font.render(f'Loading {progress:.0f}%', True, BLACK)
    #     DISPLAYSURF.blit(img, (20, 20))
    #     img2 = font.render('Solve the board and press "m" to validate', True, BLACK)
    #     DISPLAYSURF.blit(img2, (20, 50))
    #     img4 = font.render('Click cells to toggle mine location', True, BLACK)
    #     DISPLAYSURF.blit(img4, (20, 80))
    #     img5 = font.render('Arrow keys to navigate board', True, BLACK)
    #     DISPLAYSURF.blit(img5, (20, 110))
    #     img3 = font.render('Flag will be in console', True, BLACK)
    #     DISPLAYSURF.blit(img3, (20, 140))
    #     pygame.display.update()
    
    tex = f'cell{(x*y)%10}'
    cell = Cell(None, int(circuit[y][x], 16), x, y)
    validate_grid[y][x] = cell
    # if not grid.add(cell):
        # print(f'Failed to add ({x}, {y})')

offset_x = 10
offset_y = 20

travel_x = 0
travel_y = 0


def do_the_validation():
    violations = []
    
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            test_cell = validate_grid[y][x]
            if test_cell.state not in range(0, 9):
                continue
 
            neighbours = 0
            if y > 0 and x > 0: neighbours += validate_grid[y-1][x-1].state in [10, 11]
            if y > 0: neighbours += validate_grid[y-1][x].state in [10, 11]
            if y > 0 and x+1 < GRID_WIDTH: neighbours += validate_grid[y-1][x+1].state in [10, 11]
 
            if x > 0: neighbours += validate_grid[y][x-1].state in [10, 11]
            if x+1 < GRID_WIDTH: neighbours += validate_grid[y][x+1].state in [10, 11]
 
            if y+1 < GRID_HEIGHT and x > 0: neighbours += validate_grid[y+1][x-1].state in [10, 11]
            if y+1 < GRID_HEIGHT: neighbours += validate_grid[y+1][x].state in [10, 11]
            if y+1 < GRID_HEIGHT and x+1 < GRID_WIDTH: neighbours += validate_grid[y+1][x+1].state in [10, 11]
 
            if test_cell.state != neighbours:
                violations.append((x,y))
 
    if len(violations) == 0:
        bits = []
        for x in range(GRID_WIDTH):
            bit = 1 if validate_grid[23][x].state in [10, 11] else 0
            bits.append(bit)
        flag = hashlib.sha256(bytes(bits)).hexdigest()
        print(f'Flag: CTF{{{flag}}}')
 
    else:
        print(violations)
    
 
dr = [-1,1,0,0,1,1,-1,-1]
dc = [0,0,1,-1,1,-1,-1,1]

def too_many(r, c):
    if validate_grid[r][c].state >= 1 and validate_grid[r][c].state <= 8:
        count = 0 
        for i in range(len(dr)): # go through all neighbours
            newr = r + dr[i]
            newc = c + dc[i]
            if validate_grid[newr][newc].state in (10, 11): # mmin mines = no 9 plus 10 and 11
                count += 1
        return count > validate_grid[r][c].state 
    else:
        return False

def too_few(r, c, oldr, oldc):
    if validate_grid[r][c].state >= 1 and validate_grid[r][c].state <= 8:
        count = 0
        for i in range(len(dr)): # go through all neighbours
            newr = r + dr[i]
            newc = c + dc[i]
            if not((newc == oldc and newr > oldr) or newc  > oldc) and validate_grid[newr][newc].state == 9: # require that it's not the same one, and also that it comes after
                continue # skip
            if validate_grid[newr][newc].state in (9, 10, 11): # max mines = all 9 plus 10 and 11
                count += 1
        return count < validate_grid[r][c].state 
    else:
        return False

def solve(r, c):
    print(r,c)
#     print(validate_grid[r][c].state)
    if r == GRID_HEIGHT -1 and c == GRID_WIDTH - 1:
        return True

    if (r < GRID_HEIGHT - 1):
        nextr = r + 1
        nextc = c
    else:
        nextr = 0
        nextc = c + 1
    
    if validate_grid[r][c].state == 9:
#        print("here")
        # try and flag
        validate_grid[r][c].click()
        ok = True
        for i in range(len(dr)): # all neighbours
            if too_many(r + dr[i], c + dc[i]):
                ok = False
                break
        
        if not(ok) or not(solve(nextr, nextc)): # try not flagging
#            print("here2")
            validate_grid[r][c].click() # turn this one off
            ok = True
            for i in range(len(dr)): # all neighbours
                if too_few(r + dr[i], c + dc[i], r, c):
                    ok = False
                    break
            
            if not(ok):
                return False
            else:
                return solve(nextr, nextc)
        else:
            return True
    else:
        return solve(nextr, nextc)
            

def to_char(number):
    if number == 0:
        return ' '
    else:
        return hex(number).lstrip("0x").rstrip("L").upper()

for i in range(12):
    print(to_char(i))
def writeout():
    with open("output.txt", "w") as f:
        for r in range(GRID_HEIGHT):
            thisrow = ""
            for c in range(GRID_WIDTH):
                thisrow += to_char(validate_grid[r][c].state)
#             print(thisrow + "\n")
            f.write(thisrow + "\n")

sys.setrecursionlimit(100000000)
print(solve(0,0))
print("writing")
writeout()
do_the_validation()

while True: 
    offset_x += 10 * travel_x
    offset_y += 10 * travel_y
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            pos_x, pos_y = pygame.mouse.get_pos()
            cells_clicked = grid.intersectpoint((pos_x + offset_x, pos_y + offset_y))
            for c in cells_clicked:
                c.click()
                #print(c)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                travel_x = 0
            if event.key == pygame.K_RIGHT:
                travel_x = 0
            if event.key == pygame.K_UP:
                travel_y = 0
            if event.key == pygame.K_DOWN:
                travel_y = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                travel_x = -1
            if event.key == pygame.K_RIGHT:
                travel_x = 1
            if event.key == pygame.K_UP:
                travel_y = -1
            if event.key == pygame.K_DOWN:
                travel_y = 1

            if event.key == pygame.K_m:
                do_the_validation()

    DISPLAYSURF.fill(WHITE)

    # bound = DISPLAYSURF.get_bounding_rect()
    viewport = bound.move(offset_x, offset_y)

    for sprite in grid.intersect(viewport):
        sprite.draw(DISPLAYSURF, viewport)
         
    pygame.display.update()
    FramePerSec.tick(FPS)


