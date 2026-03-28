import pygame 
import math 
from queue import PriorityQueue 

width = 800
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
        return self.color == PURPLE
    
    def reset(self):
        self.color == WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        
    
    