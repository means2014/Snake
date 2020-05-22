import random
import os
import pygame
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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
        
class Snake:
    def __init__(self, head_position, direction):
        self.length = 1
        self.head = head_position
        self.direction = direction
        self.set_velocity()
        self.body = [[self.head[0]-self.velocity[0], self.head[1]-self.velocity[1]]]
        
    def set_velocity(self):
        if self.direction == 'up':
            self.velocity = [0,-1]
        elif self.direction == 'right':
            self.velocity = [1,0]
        elif self.direction == 'down':
            self.velocity = [0,1]
        elif self.direction == 'left':
            self.velocity = [-1,0]
        
    def step(self, food = None):
        self.body.insert(0, self.head)
        self.head = [self.head[0]+self.velocity[0], self.head[1]+self.velocity[1]]
        
        if self.head[0] == -1:
            print("left wall")
            return -1
        elif self.head[0] == NUM_COLS: 
            print("right wall")
            return -1
        elif self.head[1] == -1:
            print("top wall")
            return -1
        elif self.head[1] == NUM_ROWS:
            print("bottom wall")
            return -1
        elif self.head in self.body:
            print("hit self")
            return -1
        
        if self.head != food:
            self.body.pop()
            return 0
        return 1
            
    def turn(self, direction):
        if direction == self.direction:
            return
        if direction == 'left' and self.direction == 'right':
            return
        if direction == 'right' and self.direction == 'left':
            return
        if direction == 'up' and self.direction == 'down':
            return
        if direction == 'down' and self.direction == 'up':
            return
        self.direction = direction
        self.set_velocity()
        
    def draw(self, screen):
        #Draw head
        pygame.draw.polygon(screen, (0,180,60), (
            [CELL_SIZE[0]*(self.head[0]+1/2), CELL_SIZE[1]*self.head[1]], 
            [CELL_SIZE[0]*(self.head[0]+1), CELL_SIZE[1]*(self.head[1]+1/2)], 
            [CELL_SIZE[0]*(self.head[0]+1/2), CELL_SIZE[1]*(self.head[1]+1)], 
            [CELL_SIZE[0]*self.head[0], CELL_SIZE[1]*(self.head[1]+1/2)]
            ), 0)
        
        #Draw first link
        if len(self.body) > 1:
            if self.body[0][0] == self.body[1][0]:
                if self.body[1][1] == self.body[0][1]+1:
                    p1 = [CELL_SIZE[0]*(self.body[1][0]), CELL_SIZE[1]*(self.body[1][1])]
                    p2 = [CELL_SIZE[0]*(self.body[1][0]+1), CELL_SIZE[1]*(self.body[1][1])]
                    p3 = [CELL_SIZE[0]*(self.body[0][0]+1/2), CELL_SIZE[1]*(self.body[0][1])]
                else:
                    p1 = [CELL_SIZE[0]*(self.body[1][0]), CELL_SIZE[1]*(self.body[1][1]+1)]
                    p2 = [CELL_SIZE[0]*(self.body[1][0]+1), CELL_SIZE[1]*(self.body[1][1]+1)]
                    p3 = [CELL_SIZE[0]*(self.body[0][0]+1/2), CELL_SIZE[1]*(self.body[0][1]+1)]
            elif self.body[0][0] == self.body[1][0]-1:
                p1 = [CELL_SIZE[0]*(self.body[1][0]), CELL_SIZE[1]*(self.body[1][1])]
                p2 = [CELL_SIZE[0]*(self.body[1][0]), CELL_SIZE[1]*(self.body[1][1]+1)]
                p3 = [CELL_SIZE[0]*self.body[0][0], CELL_SIZE[0]*(self.body[0][1]+1/2)]
            else:
                p1 = [CELL_SIZE[0]*(self.body[1][0]+1), CELL_SIZE[1]*(self.body[1][1]+1)]
                p2 = [CELL_SIZE[0]*(self.body[1][0]+1), CELL_SIZE[1]*(self.body[1][1])]
                p3 = [CELL_SIZE[0]*(self.body[0][0]+1), CELL_SIZE[0]*(self.body[0][1]+1/2)]
            pygame.draw.polygon(screen, (0,180,60), (p1, p2, p3), 0)
        
        
        #Draw body
        for cell in self.body[1:-1]:
            pygame.draw.rect(screen, (0, 180, 60), (cell[0]*CELL_SIZE[0], cell[1]*CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]), 0)
            pygame.draw.polygon(screen, (228,255,20), (
                [CELL_SIZE[0]*(cell[0]+1/2), CELL_SIZE[1]*cell[1]], 
                [CELL_SIZE[0]*(cell[0]+1), CELL_SIZE[1]*(cell[1]+1/2)], 
                [CELL_SIZE[0]*(cell[0]+1/2), CELL_SIZE[1]*(cell[1]+1)], 
                [CELL_SIZE[0]*cell[0], CELL_SIZE[1]*(cell[1]+1/2)]
                ), 1)
            
        #Draw Tail
        #Moving Down
            if self.body[-2][0] == self.body[-1][0]:
                if self.body[-2][1] == self.body[-1][1]+1:
                    p1 = [CELL_SIZE[0]*self.body[-2][0], CELL_SIZE[1]*self.body[-2][1]]
                    p2 = [CELL_SIZE[0]*(self.body[-2][0]+1), CELL_SIZE[1]*self.body[-2][1]]
                    p3 = [CELL_SIZE[0]*(self.body[-1][0]+1/2), CELL_SIZE[1]*self.body[-1][1]]
        #Moving UP
                else:
                    p1 = [CELL_SIZE[0]*self.body[-1][0], CELL_SIZE[1]*(self.body[-2][1]+1)]
                    p2 = [CELL_SIZE[0]*(self.body[-2][0]+1), CELL_SIZE[1]*(self.body[-2][1]+1)]
                    p3 = [CELL_SIZE[0]*(self.body[-1][0]+1/2), CELL_SIZE[1]*(self.body[-1][1]+1)]
        #Moving Left
            elif self.body[-2][0] == self.body[-1][0]-1:
                p1 = [CELL_SIZE[0]*(self.body[-2][0]+1), CELL_SIZE[1]*self.body[-2][1]]
                p2 = [CELL_SIZE[0]*(self.body[-2][0]+1), CELL_SIZE[1]*(self.body[-2][1]+1)]
                p3 = [CELL_SIZE[0]*(self.body[-1][0]+1), CELL_SIZE[1]*(self.body[-1][1]+1/2)]
        #Moving Right
            else:
                p1 = [CELL_SIZE[0]*self.body[-2][0], CELL_SIZE[1]*self.body[-2][1]]
                p2 = [CELL_SIZE[0]*self.body[-2][0], CELL_SIZE[1]*(self.body[-2][1]+1)]
                p3 = [CELL_SIZE[0]*self.body[-1][0], CELL_SIZE[1]*(self.body[-1][1]+1/2)]
            pygame.draw.polygon(screen, (0,180,60), (p1, p2, p3), 0)

if __name__ == '__main__':
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    NUM_ROWS = 50
    NUM_COLS = 50
    CELL_SIZE = [SCREEN_WIDTH//NUM_COLS, SCREEN_HEIGHT//NUM_ROWS]
    
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Python')
    screen.fill((255,255,255))
    
    board = init_board(NUM_COLS, NUM_ROWS)
    
    #Draw the empty board
    for i in range(NUM_COLS):
        for j in range(NUM_ROWS):
            pygame.draw.rect(screen, (0,0,0), (i*CELL_SIZE[0], j*CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]), 0)
            
    #Initialize Snake with random position
    player = Snake(random_pos(NUM_COLS, NUM_ROWS), random_direction())
    player.draw(screen)
    
    #Initialize food position
    food = random_pos(NUM_COLS, NUM_ROWS)
    pygame.draw.rect(screen, (180, 0, 0), (food[0]*CELL_SIZE[0], food[1]*CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]), 0)
    
    clock = pygame.time.Clock()
    
    playing = True
    while playing:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.turn('left')
                if event.key == pygame.K_RIGHT:
                    player.turn('right')
                if event.key == pygame.K_UP:
                    player.turn('up')
                if event.key == pygame.K_DOWN:
                    player.turn('down') # for what
        
        step = player.step(food)
        if step == -1:
            #Failed, display score and prompt to play again or close
            Tk().wm_withdraw()
            
            result = messagebox.askokcancel('Game over', ('Final Score '+str(len(player.body)-2)+'\n\nPlay again?'))
            if result:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                game_over = True
                while game_over:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                            game_over = False
                            break            
            pygame.quit()
        elif step == 1:
            food = random_pos(NUM_COLS, NUM_ROWS)
            while food in player.body or food == player.head:
                food = random_pos(NUM_COLS, NUM_ROWS)
            
        for i in range(NUM_COLS):
            for j in range(NUM_ROWS):
                pygame.draw.rect(screen, (0,0,0), (i*CELL_SIZE[0], j*CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]), 0)
                
        
        pygame.draw.rect(screen, (180, 0, 0), (food[0]*CELL_SIZE[0], food[1]*CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]), 0)
        player.draw(screen)
        
        pygame.display.flip()
        
        #Speed up as snake grows
        clock.tick(5+2*len(player.body))
        
    pygame.quit()