#    Main Author(s): Ziyang Wang, Wilgard Fils-aime, Jaehyuk Heo
#    Main Reviewer(s):Jaehyuk Heo


import pygame
import sys
import math
import os

from partD import overflow
from partC import Queue, Stack  # Stack 클래스를 가져옴
from player1 import PlayerOne
from player2 import PlayerTwo 

class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], 1, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        return self.current_option

class Board:
    def __init__(self, width, height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height - 1][self.width - 1] = -1
        self.turn = 0
        self.history = Stack()  

    def get_board(self):
        current_board = []
        for i in range(self.height):
            current_board.append(self.board[i].copy())
        return current_board

    def valid_move(self, row, col, player):
        if row >= 0 and row < self.height and col >= 0 and col < self.width and (self.board[row][col] == 0 or self.board[row][col] / abs(self.board[row][col]) == player):
            return True
        return False

    def add_piece(self, row, col, player):
        if self.valid_move(row, col, player):
            self.history.push(self.get_board())  
            self.board[row][col] += player
            self.turn += 1
            return True
        return False

    def undo_move(self):
        if not self.history.is_empty():
            self.board = self.history.pop()  

    def check_win(self):
        if self.turn > 0:
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j] > 0:
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif self.board[i][j] < 0:
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if num_p1 == 0:
                return -1
            if num_p2 == 0:
                return 1
        return 0

    def do_overflow(self, q):
        oldboard = []
        for i in range(self.height):
            oldboard.append(self.board[i].copy())
        numsteps = overflow(self.board, q)
        if numsteps != 0:
            self.set(oldboard)
        return numsteps

    def set(self, newboard):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE + Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    if self.board[row][col] > 0:
                        sprite = self.p1_sprites
                    else:
                        sprite = self.p2_sprites
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE // 2 - 16
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

                    elif abs(self.board[row][col]) == 3:
                        cpos += CELL_SIZE // 2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        cpos += CELL_SIZE // 2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):  # 패키징된 실행 파일일 때
        base_path = sys._MEIPASS
    else:  # 개발 환경에서 실행될 때
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


GRID_SIZE = (5, 6)
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5


p1spritesheet = pygame.image.load(resource_path('blue.png'))
p2spritesheet = pygame.image.load(resource_path('pink.png'))
p1_sprites = []
p2_sprites = []

player_id = [1, -1]

for i in range(8):
    curr_sprite = pygame.Rect(32 * i, 0, 32, 32)
    p1_sprites.append(p1spritesheet.subsurface(curr_sprite))
    p2_sprites.append(p2spritesheet.subsurface(curr_sprite))

frame = 0


pygame.init()
window = pygame.display.set_mode((1200, 800))

pygame.font.init()
font = pygame.font.Font(None, 36)  # Change the size as needed
bigfont = pygame.font.Font(None, 108)

player1_dropdown = Dropdown(900, 50, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Human', 'AI'])


class PlayerOne:
    def __init__(self):
        self.smartness = 1

    def get_play(self, board):
        return (0, 0)  

class PlayerTwo:
    def __init__(self):
        self.smartness = 1

    def get_play(self, board):
        return (0, 0) 

p1_smartness_level = "Beginner"
p2_smartness_level = "Beginner"


def set_p1_smartness(level):
    global p1_smartness_level
    print(f"Setting Player 1 smartness to {level}")  
    p1_smartness_level = level
    if level == 'Beginner':
        bots[0].smartness = 1  
    elif level == 'Intermediate':
        bots[0].smartness = 5  
    elif level == 'Advanced':
        bots[0].smartness = 10  

def set_p2_smartness(level):
    global p2_smartness_level
    print(f"Setting Player 2 smartness to {level}") 
    p2_smartness_level = level
    if level == 'Beginner':
        bots[1].smartness = 1
    elif level == 'Intermediate':
        bots[1].smartness = 5  
    elif level == 'Advanced':
        bots[1].smartness = 10 

status = ["", ""]
current_player = 0
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)

running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE


                if 900 <= x <= 1100 and 200 <= y <= 250:
                    board.undo_move()


                elif 900 <= x <= 1100 and 300 <= y <= 350:
                    set_p1_smartness('Beginner')
                elif 900 <= x <= 1100 and 370 <= y <= 420:
                    set_p1_smartness('Intermediate')
                elif 900 <= x <= 1100 and 440 <= y <= 490:
                    set_p1_smartness('Advanced')


                elif 900 <= x <= 1100 and 510 <= y <= 560:
                    set_p2_smartness('Beginner')
                elif 900 <= x <= 1100 and 580 <= y <= 630:
                    set_p2_smartness('Intermediate')
                elif 900 <= x <= 1100 and 650 <= y <= 700:
                    set_p2_smartness('Advanced')

    win = board.check_win()
    if win != 0:
        winner = 1
        if win == -1:
            winner = 2
        has_winner = True

    if not has_winner:
        if overflowing:
            status[0] = "Overflowing"
            if not overflow_boards.is_empty():
                if repeat_step == FULL_DELAY:
                    next = overflow_boards.dequeue()
                    board.set(next)
                    repeat_step = 0
                else:
                    repeat_step += 1
            else:
                overflowing = False
                current_player = (current_player + 1) % 2

        else:
            status[0] = "Player " + str(current_player + 1) + "'s turn"
            make_move = False
            if choice[current_player] == 1:
                (grid_row, grid_col) = bots[current_player].get_play(board.get_board())
                status[1] = "Bot chose row {}, col {}".format(grid_row, grid_col)
                if not board.valid_move(grid_row, grid_col, player_id[current_player]):
                    has_winner = True
                    winner = ((current_player + 1) % 2) + 1
                else:
                    make_move = True
            else:
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True

            if make_move:
                board.add_piece(grid_row, grid_col, player_id[current_player])
                numsteps = board.do_overflow(overflow_boards)
                if numsteps != 0:
                    overflowing = True
                    repeat_step = 0
                else:
                    current_player = (current_player + 1) % 2
                grid_row = -1
                grid_col = -1


    window.fill(WHITE)
    board.draw(window, frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))
    frame = (frame + 0.5) % 8
    player1_dropdown.draw(window)
    player2_dropdown.draw(window)
    pygame.draw.rect(window, BLACK, (900, 200, 200, 50), 2)  
    text = font.render('Undo', True, BLACK)
    window.blit(text, (905, 205))
    

    pygame.draw.rect(window, BLACK, (900, 300, 200, 50), 2)
    text = font.render('P1 Beginner', True, BLACK)
    window.blit(text, (905, 305))
    pygame.draw.rect(window, BLACK, (900, 370, 200, 50), 2)
    text = font.render('P1 Intermediate', True, BLACK)
    window.blit(text, (905, 375))
    pygame.draw.rect(window, BLACK, (900, 440, 200, 50), 2)
    text = font.render('P1 Advanced', True, BLACK)
    window.blit(text, (905, 445))
    pygame.draw.rect(window, BLACK, (900, 510, 200, 50), 2)
    text = font.render('P2 Beginner', True, BLACK)
    window.blit(text, (905, 515))
    pygame.draw.rect(window, BLACK, (900, 580, 200, 50), 2)
    text = font.render('P2 Intermediate', True, BLACK)
    window.blit(text, (905, 585))
    pygame.draw.rect(window, BLACK, (900, 650, 200, 50), 2)
    text = font.render('P2 Advanced', True, BLACK)
    window.blit(text, (905, 655))


    p1_smartness_text = font.render(f"P1 Smartness: {p1_smartness_level}", True, BLACK)
    p2_smartness_text = font.render(f"P2 Smartness: {p2_smartness_level}", True, BLACK)
    window.blit(p1_smartness_text, (900, 710))
    window.blit(p2_smartness_text, (900, 740))

    if not has_winner:
        text = font.render(status[0], True, (0, 0, 0))
        window.blit(text, (X_OFFSET, 750))
        text = font.render(status[1], True, (0, 0, 0))
        window.blit(text, (X_OFFSET, 700))
    else:
        text = bigfont.render("Player " + str(winner) + " wins!", True, (0, 0, 0))
        window.blit(text, (300, 250))

    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
