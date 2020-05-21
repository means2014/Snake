import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
NUM_ROWS = 50
NUM_COLS = 50
CELL_SIZE = (SCREEN_WIDTH/NUM_COLS, SCREEN_HEIGHT/NUM_ROWS)

def init_board(width, height):
    board = [0]*width
    board[0] = [-1]*height
    board[height-1] = [-1]*height
    
    for i in range(1, height-1):
        board[i] = [0]*height
        board[i][0] = -1
        board[i][height-1] = -1
        
def random_pos(cols, rows):
    x = random.randrange(cols)
    y = random.randrange(rows)
    return [x,y]
    
def random_direction():
    return random.choice(['up', 'down', 'left', 'right'])
        
class snake:
    def __init__(self, head_position, direction):
        self.length = 1
        self.head = head_position
        self.direction = direction
        self.body = []
        
    def set_velocity(self):
        if self.direction == 'up':
            self.velocity = [0,-1]
        elif self.direction == 'right':
            self.velocity = [1,0]
        elif self.direction == 'down':
            self.velocity = [0,1]
        elif self.direction == 'left':
            self.velocity = [-1,0]
        
    def step(self, food = False):
        self.body.insert(0, self.head)
        self.head = [self.head[0]+self.velocity[0], self.head[1]+self.velocity[1]]
        if not food:
            self.body.pop()
            
    def turn(self, direction):
        self.direction = direction
        self.set_velocity()