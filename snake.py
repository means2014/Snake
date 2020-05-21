import random

def init_board(width, height):
    board = [0]*width
    board[0] = [-1]*height
    board[height-1] = [-1]*height
    
    for i in range(1, height-1):
        board[i] = [0]*height
        board[i][0] = -1
        board[i][height-1] = -1
        
    return board
        
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
        self.set_velocity()
        
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
        
    def draw(self, screen):
        #Draw head
        HEAD_WIDTH = 0.6
        EYE_RADIUS = 0.1
        if self.direction == 'down':
            pygame.draw.ellipse(screen, (0, 180, 60), (CELL_SIZE[0]*(self.head[0]+(1-HEAD_WIDTH)), CELL_SIZE[1]*self.head[1], CELL_SIZE[0]*HEAD_WIDTH, CELL_SIZE[1]), 0)
            
            c1x = CELL_SIZE[0]*(self.head[0]+0.4)
            c2x = CELL_SIZE[0]*(self.head[0]+0.6)
            c1y = CELL_SIZE[1]*(self.head[1]+0.8)
            c2y = CELL_SIZE[1]*(self.head[1]+0.8)
            
        elif self.direction == 'up':
            pygame.draw.ellipse(screen, (0, 180, 60), (CELL_SIZE[0]*(self.head[0]+(1-HEAD_WIDTH)), CELL_SIZE[1]*self.head[1], CELL_SIZE[0]*HEAD_WIDTH, CELL_SIZE[1]), 0)
            
            c1x = CELL_SIZE[0]*(self.head[0]+0.4)
            c2x = CELL_SIZE[0]*(self.head[0]+0.6)
            c1y = CELL_SIZE[1]*(self.head[1]+0.2)
            c2y = CELL_SIZE[1]*(self.head[1]+0.2)
            
        elif self.direction == 'left':
            pygame.draw.ellipse(screen, (0, 180, 60), (CELL_SIZE[0]*self.head[0], CELL_SIZE[1]*(self.head[1]+(1-HEAD_WIDTH)), CELL_SIZE[0], CELL_SIZE[1]*HEAD_WIDTH), 0)
            
            c1x = CELL_SIZE[0]*(self.head[0]+0.2)
            c2x = CELL_SIZE[0]*(self.head[0]+0.2)
            c1y = CELL_SIZE[1]*(self.head[1]+0.4)
            c2y = CELL_SIZE[1]*(self.head[1]+0.6)
            
        else:
            pygame.draw.ellipse(screen, (0, 180, 60), (CELL_SIZE[0]*self.head[0], CELL_SIZE[1]*(self.head[1]+(1-HEAD_WIDTH)), CELL_SIZE[0], CELL_SIZE[1]*HEAD_WIDTH), 0)
            
            c1x = CELL_SIZE[0]*(self.head[0]+0.8)
            c2x = CELL_SIZE[0]*(self.head[0]+0.8)
            c1y = CELL_SIZE[1]*(self.head[1]+0.4)
            c2y = CELL_SIZE[1]*(self.head[1]+0.6)
            
        pygame.draw.circle(screen, (255,255,255), (c1x, c1y), EYE_RADIUS, 0)
        pygame.draw.circle(screen, (0,0,0), (c1x, c1y), EYE_RADIUS/10, 0)
            
        pygame.draw.circle(screen, (255,255,255), (c2x, c2y), EYE_RADIUS, 0)
        pygame.draw.circle(screen, (0,0,0), (c2x, c2y), EYE_RADIUS/10, 0)
        
        #Draw body
        for cell in self.body[0:-1]
            pygame.draw.rect(screen, (0, 180, 60), (cell[0]*CELL_SIZE[0], cell[1]*CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]), 0)
            pygame.draw.polygon(screen, (228,255,20), ([CELL_SIZE[0]*(cell[0]+1/2), CELL_SIZE[1]*cell[1]], [CELL_SIZE[0]*cell[0], CELL_SIZE[1]*(cell[1]+1/2)], [CELL_SIZE[0]*(cell[0]+1/2), CELL_SIZE[1]*(cell[1]+1)], [CELL_SIZE[0]*(cell[0] + 1/2), CELL_SIZE[1]*(cell[0]+1/2)]), 1)
            
        #Draw Tail
        #Moving Down
            if self.body[-2][0] == self.body[-1][0]:
                if self.body[-2][1] == self.body[-1][1]+1:
                    p1 = [CELL_SIZE[0]*self.body[-2][0], CELL_SIZE[1]*self.body[-2][1]]
                    p2 = [CELL_SIZE[0]*(self.body[-2][0]+1), CELL_SIZE[1]*self.body[-2][1]]
                    p3 = [CELL_SIZE[0]*(self.body[-1][0]+1/2), CELL_SIZE[1]*self.body[-1]]
        #Moving UP
                else:
                    p1 = [CELL_SIZE[0]*self.body[-1][0], CELL_SIZE[1]*(self.body[-2][1]+1)]
                    p2 = [CELL_SIZE[0]*(self.body[-2][0]+1), CELL_SIZE[1]*(self.body[-2][1]+1)]
                    p3 = [CELL_SIZE[0]**(self.body[-1][0]+1/2), CELL_SIZE[1]*(self.body[-1]+1)]
        #Moving Left
            elif self.body[-2][0] == self.body[-1][0]-1:
                p1 = [CELL_SIZE[0]*(self.body[-2][0]+1), CELL_SIZE[1]*self.body[-2][1]]
                p2 = [CELL_SIZE[0]*(self.body[-2][0]+1), CELL_SIZE[1]*(self.body[-2][1]+1)]
                p3 = [CELL_SIZE[0]*(self.body[-1][0]+1), CELL_SIZE[1]*(self.body[-1][1]+1/2)]
        #Moving Right
            else:
                p1 = [CELL_SIZE[0]*self.body[-2][0], CELL_SIZE[1]*self.body[-2][1]]
                p2 = [CELL_SIZE[0]*self.body[-1][0], CELL_SIZE[1]*(self.body[-2][1]+1)]
                p3 = [CELL_SIZE[0]*self.body[-1][0], CELL_SIZE[1]*(self.body[-1][1]+1/2)]
        pygame.draw.polygon(screen, (0,180,60), (p1, p2, p3), 0)

if __name__ == '__main__':
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    NUM_ROWS = 50
    NUM_COLS = 50
    CELL_SIZE = (SCREEN_WIDTH/NUM_COLS, SCREEN_HEIGHT/NUM_ROWS)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    board = init_board(NUM_COLS, NUM_ROWS)
    
    #Draw the empty board
    for i in range(NUM_COLS):
        for j in range(NUM_ROWS):
            pygame.draw.rect(screen, (255,255,255), (i*CELL_SIZE[0], j*CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]), 1)
            
    #Initialize Snake with random position
    player = Snake(random_pos(NUM_COLS, NUM_ROWS), random_direction())
    player.draw(screen)
    
    #Initialize food position
    food = random_pos(NUM_COLS, NUM_ROWS)
    pygame.draw.rect(screen, (180, 0, 0), (food[0]*CELL_SIZE[0], food[1]*CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]), 0)