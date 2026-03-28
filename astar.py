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
        self.color = WHITE

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
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_barrier():#checking if we can move down
            self.neighbors.append(grid[self.row + 1][self.column])

        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier():#checking if we can move up
            self.neighbors.append(grid[self.row - 1][self.column])

        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_barrier():#checking if we can move right
            self.neighbors.append(grid[self.row][self.column + 1])

        if self.column > 0 and not grid[self.row][self.column - 1].is_barrier():#checking if we move left
            self.neighbors.append(grid[self.row][self.column - 1])

    def __lt__(self, other):#lt stand for less than btw its a dunder method
        return False
    
    
def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start_position, end_position):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_position))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start_position] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start_position] = heuristic(start_position.get_position(), end_position.get_position())

    open_set_hash = {start_position}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end_position:
            reconstruct_path(came_from, end_position, draw)
            end_position.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end_position.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put(f_score[neighbor], count, neighbor)
                    open_set_hash.add(neighbor)
                    neighbor.make_closed()
        
        draw()

        if current != start_position:
            current.make_closed()

    return False


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
                if not start_position and node != end_position:
                    start_position = node
                    start_position.make_start()

                elif not end_position and node != start_position:
                    end_position = node
                    end_position.make_end()

                elif node != end_position and node != start_position:
                    node.make_barrier()


            elif pygame.mouse.get_pressed()[2]:#right
                position = pygame.mouse.get_pos()
                row, column = get_clicked_position(position, rows, width)
                node = grid[row][column]
                node.reset()
                if node == start_position:
                    start_position = None

                if node == end_position:
                    end_position = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(window, grid, rows, width), grid, start_position, end_position)
                    

    pygame.quit()

main(window, width)