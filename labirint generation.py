import pygame as pg
from random import choice


WIDTH, HEIGHT = 1002, 802
TILE = 20
cols, rows = WIDTH // TILE, HEIGHT // TILE


class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.visited = False

        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}

    def draw(self):
        x0 = TILE * self.x
        y0 = TILE * self.y

        if self.visited:
            pg.draw.rect(sc, pg.Color('aquamarine'), (x0, y0, TILE, TILE))
        if self.walls['top']:
            pg.draw.line(sc, pg.Color('darkorange'), (x0, y0), (x0 + TILE, y0), 2)
        if self.walls['right']:
            pg.draw.line(sc, pg.Color('darkorange'), (x0 + TILE, y0), (x0 + TILE, y0 + TILE), 2)
        if self.walls['bottom']:
            pg.draw.line(sc, pg.Color('darkorange'), (x0, y0 + TILE), (x0 + TILE, y0 + TILE), 2)
        if self.walls['left']:
            pg.draw.line(sc, pg.Color('darkorange'), (x0, y0), (x0, y0 + TILE), 2)

    def draw_current(self):
        x0, y0 = self.x * TILE, self.y * TILE
        pg.draw.rect(sc, pg.Color('deepskyblue'), (x0, y0, TILE, TILE))

    def find_unvisited_neighbor(self):
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        arr = []
        for cell in [top, right, bottom, left]:
            if cell and not cell.visited:
                arr.append(cell)

        return choice(arr) if arr else False

    @staticmethod
    def check_cell(x, y):
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return cells[x + y * cols]


def remove_walls(current, next):
    dx = current.x - next.x
    dy = current.y - next.y

    if dx == 1:
        current.walls['left'] = next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = next.walls['left'] = False
    elif dy == 1:
        current.walls['top'] = next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = next.walls['top'] = False


pg.init()
sc = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


cells = [Cell(i, j) for j in range(rows) for i in range(cols)]
curr_cell = cells[0]
curr_cell.visited = True
stack = [curr_cell]

while stack:
    next_cell = curr_cell.find_unvisited_neighbor()
    if next_cell:
        next_cell.visited = True
        remove_walls(curr_cell, next_cell)
        curr_cell = next_cell
        stack += [curr_cell]
    else:
        curr_cell = stack.pop()

while True:
    sc.fill(pg.Color('thistle'))

    for event in pg.event.get():
        if event.type == pg.QUIT:
             exit()

    for cell in cells:
        cell.draw()

    clock.tick(30)
    pg.display.flip()
