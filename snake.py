import pygame
import random
import  math
import tkinter as tk
from tkinter import  messagebox

class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255,255,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=True):
        dis = self.w // self.rows
        i = self.pos[0] # rows
        j = self.pos[1] # columns, do make sense when imagine i,j as x,y

        pygame.draw.rect(surface, self.color, (i*dis +1, j*dis+1, dis-1 , dis -2)) # +1 for, if not border lines fo squares will be covered by cubes

        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i*dis + center - radius, j*dis+8)
            circleMiddle2 = (i * dis + dis - radius*2, j * dis + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) # head of the snake
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1 # at the same time snake can only move in one direction

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # turning the head of the snake


                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): # self.body is a cube object.
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:   # checking the edge of the screen and placing the snake
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1 , c.pos[1]) # dirn efers to snake class self.head.pos , dirnx, dirny changes in cube.mov metod
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1 : c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], c.pos[1])
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx, c.dirny) # if not move along the direction without turning


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # Checking whether what direction currently snake is moving
        # Left , Right , Up , Down and adding a cube(when eat a snack) according to it.
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i==0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows # size between lines in the grid

    x= 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w)) # vertical white  line (top to bottom)
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y)) # horizontal lines (left to right)

def redrawWindow(surface):
    global rows, width, s , snack # If we make these global we don't always want to pass these into method parameters
    surface.fill((0,0,0)) # black in colour
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows ,surface)
    pygame.display.update()

def randomsnack(rows, item):

    positions = item.body # Get all the positions of cubes in our snake

    while True:  # Keep generating random positions until we get a valid one
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda z:z.pos == (x, y), positions)))> 0:
            # This wll check if the position we generated is occupied by the snake
            continue
        else:
            break
    return  (x, y)



def message_box(subject, content):
    root = tk.Tk
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows , s, snack
    width = 500 # we don't want height, on square width = height

    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0),(10,10))  # red in colour and 10, 10 position
    snack = cube(randomsnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomsnack(rows, s), color = (0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score:', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                break
        redrawWindow(win)

main()