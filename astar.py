import pygame 
import math 
from queue import PriorityQueue 

width = 600
window = pygame.display.set_mode((width, width))
pygame.display.set_caption("A* Star Path Finding Algorithim")

#COLORS 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.x = row * width #x coordinate
        self.y = column * width #y coordinate
        self.color = WHITE 
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):#basically to help in indexing/ identifying
        return self.row, self.column
    
    def is_closed(self):#basically checking if it has been visited
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start_node(self):
        return self.color == ORANGE
    
    def is_end_node(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color == WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):#lt stand for less than btw its a dunder method
        return False
    
def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):#draws grid lines
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):#draws grid lines
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width):#draws everything
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()

def get_clicked_position(position, rows, width):
    gap = width // rows
    y, x = position

    row = y // gap
    column = x // gap

    return row, column


def main(window, width):
    rows = 50
    grid = make_grid(rows, width)# u can modify the size directly here by changing size of rows

    start_position = None
    end_position = None 

    run = True
    started = False

    while run:
        draw(window, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:#left
                position = pygame.mouse.get_pos()
                row, column = get_clicked_position(position, rows, width)
                node = grid[row][column]
                if not started:
                    start = node
                    start.make_start()

                elif not end:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()


            elif pygame.mouse.get_pressed()[2]:#right
                pass



    pygame.quit()

main(window, width)