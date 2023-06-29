import random

import pygame
from grid import Grid
# PYGAME INIT....


# Pygame Init
pygame.init()
SCREEN_SIZE = (530,600)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.NOFRAME)
running = True

# Essential gamePlay Variables
GRID_SIZE = 120
score = 0
Lost = False
Win = False
btn = pygame.Rect(310,540,100,50)
btn_close = pygame.Rect(420,540,100,50)

# Make a board
board = []
def make_new_game():
    global board,score
    while board:
        board.pop()
    score = 0
    for  i in range(0,4):
        row = []
        for j in range(0,4):
            x = j * GRID_SIZE + (j+1) *10
            y = i * GRID_SIZE + (i+1) *10
            rect = pygame.Rect(x,y,GRID_SIZE,GRID_SIZE)
            grid = Grid(0,(i,j),rect,GRID_SIZE)
            row.append(grid)
        board.append(row)
    if add_new_number_to_board(2, 0) == -1:
        print("GameOver")

def add_new_number_to_board(number,flag):
    empty_spots = []
    global board
    for ii,i in enumerate(board):
        for jj ,j in enumerate(i):
            if j.number == 0:
                empty_spots.append([ii,jj])

    if empty_spots != []:
        for k in range(0,number):
            random_empty_spot = random.choice(empty_spots)
            empty_spots.remove(random_empty_spot)
            if flag == 0:
                rand_no = random.choice([2,4])
            else:
                rand_no = 2
            board[random_empty_spot[0]][random_empty_spot[1]].change_number(rand_no)
    else:
        return -1

def draw_game(screen,board):
    for ii, i in enumerate(board):
        for jj, j in enumerate(i):
            pygame.draw.rect(screen,j.BGcolor,j.rect,border_radius=3)
            if j.number !=0:
                text = pygame.font.Font('./MainFont2.ttf', 40).render(f'{j.number}', True, (0, 0,0), j.BGcolor)
                textRect = text.get_rect()
                textRect.left = j.rect.left + GRID_SIZE /2 - textRect.width/2
                textRect.top = j.rect.top  + GRID_SIZE/2 - textRect.height/2
                screen.blit(text, textRect)

def make_move(move):
    global running,Lost,Win
    if move == "l":
        print(f"Your Move ==>Left")
        for ii,i in enumerate(board):
            filter_lst = slide_move(i,1,True)
            filter_lst = join_move(filter_lst,1)
            filter_lst = slide_move(filter_lst,0,True)
            for jj,j in enumerate(i):
                j.change_number(filter_lst[jj])


    elif move == "r":
        print("Your Move ==>Right")
        for ii,i in enumerate(board):
            filter_lst = slide_move(i, 1, False)
            filter_lst = join_move(filter_lst,1)
            filter_lst = slide_move(filter_lst, 0, False)
            for jj,j in enumerate(i):
                j.change_number(filter_lst[jj])

    elif move == "u":
        print("Your Move ==>Up")
        column = []
        for jj,j in enumerate(board):
            for ii,i in enumerate(j):
                column.append(board[ii][jj])
            filter_lst = slide_move(column, 1, True)
            filter_lst = join_move(filter_lst,1)
            filter_lst = slide_move(filter_lst, 0, True)
            for l in range(4):
                board[l][jj].change_number(filter_lst[l])
            column = []
    elif move == "d":
        print("Your Move ==>DOWN")
        column = []
        for jj,j in enumerate(board):
            for ii,i in enumerate(j):
                column.append(board[ii][jj])
            filter_lst = slide_move(column, 1, False)
            filter_lst = join_move(filter_lst,1)
            filter_lst = slide_move(filter_lst, 0, False)
            for l in range(4):
                board[l][jj].change_number(filter_lst[l])
            column = []


    add_new_number_to_board(1,1)
    win_dirs = {
        1:"Won the Match!!",
        0:"Continue Playing!!",
        -1:"You lost the Match!!"
    }
    win = check_win()

    if win ==-1:
        print(win_dirs[win])
        Lost = True
    if win ==1:
        Win = True

def check_win():
    global running
    win = check_win_lose(board)
    if win == 1:
        return 1
    moves_present = False

    for ii, i in enumerate(board):
        filter_lst = slide_move(i, 1, True)
        filter_lst = join_move(filter_lst,0)
        filter_lst = slide_move(filter_lst, 0, True)
        for k in filter_lst:
            if k == 0:
                moves_present = True
                return 0

    for ii, i in enumerate(board):
        filter_lst = slide_move(i, 1, False)
        filter_lst = join_move(filter_lst,0)
        filter_lst = slide_move(filter_lst, 0, False)
        for k in filter_lst:
            if k == 0:
                moves_present = True
                return 0

    column = []
    for jj, j in enumerate(board):
        for ii, i in enumerate(j):
            column.append(board[ii][jj])
        filter_lst = slide_move(column, 1, True)
        filter_lst = join_move(filter_lst,0)
        filter_lst = slide_move(filter_lst, 0, True)
        for k in filter_lst:
            if k == 0:
                moves_present = True
                return 0
        column = []

    column = []
    for jj, j in enumerate(board):
        for ii, i in enumerate(j):
            column.append(board[ii][jj])
        filter_lst = slide_move(column, 1, False)
        filter_lst = join_move(filter_lst,0)
        filter_lst = slide_move(filter_lst, 0, False)
        for k in filter_lst:
            if k == 0:
                moves_present = True
                return 0
        column = []

    return -1

def slide_move(row,flag,last):
    filter_lst = [j.number for j in row if j.number != 0] if flag == 1 else [j for j in row if j != 0]

    missing = 4 - len(filter_lst)
    for k in range(missing):
        if last == True:
            filter_lst.append(0)
        else:
            filter_lst.insert(0,0)

    return filter_lst

def join_move(row,flag):
    global score

    for ii,i in enumerate(row):
        if i !=0 and ii !=3:
                if i == row[ii+1]:

                    if flag == 1:
                        score += 2 * row[ii]
                    row[ii] = 2 * row[ii]
                    row[ii+1] = 0

    return row

def draw_score(score,screen):
    text = pygame.font.Font('./MainFont.ttf', 40).render(f'Score: {score}', True, (0, 0, 0), (255,255,255))
    textRect = text.get_rect()
    textRect.top = 540
    textRect.left = 10
    screen.blit(text, textRect)


def click_func(pos):
    global running
    if btn.collidepoint(pos):
        make_new_game()

    elif btn_close.collidepoint(pos):
        running = False
def check_win_lose(board):
    for ii,i in enumerate(board):
        for jj,j in enumerate(i):
            if j.number >= 2048:
                return 1
make_new_game()


while running:
    clock.tick(60)
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                make_move('u')
            elif event.key == pygame.K_DOWN:
                make_move('d')
            elif event.key == pygame.K_LEFT:
                make_move('l')
            elif event.key == pygame.K_RIGHT:
                make_move('r')
        if event.type == pygame.MOUSEBUTTONUP:
            click_func(event.pos)
    # Button
    pygame.draw.rect(screen,(0,0,0),btn,border_radius=5)
    text = pygame.font.Font('./MainFont.ttf', 26).render(f'New Game', True,  (255, 255, 255),(0, 0, 0),)
    textRect = text.get_rect()
    textRect.top = 565 - textRect.height/2
    textRect.left = 360 - textRect.width/2
    screen.blit(text, textRect)

    pygame.draw.rect(screen,(0,0,0),btn_close,border_radius=5)
    text = pygame.font.Font('./MainFont.ttf', 26).render(f'Close', True,  (255, 255, 255),(0, 0, 0))
    textRect = text.get_rect()
    textRect.top = 565- textRect.height/2
    textRect.left = 470 - textRect.width/2
    screen.blit(text, textRect)

    draw_game(screen,board)
    draw_score(score,screen)

    if Lost == True:
        text = pygame.font.Font('./MainFont.ttf', 40).render(f'You Lost the match!!', True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.top = 300 - textRect.height/2
        textRect.left = 530/2 - textRect.width/2
        screen.blit(text, textRect)
        pygame.display.update()
        pygame.time.wait(2500)
        make_new_game()
        Lost = False


    if Win == True:
        text = pygame.font.Font('./MainFont.ttf', 40).render(f'You Won the match!!', True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.top = 300 - textRect.height/2
        textRect.left = 530/2 - textRect.width/2
        screen.blit(text, textRect)
        pygame.display.update()
        pygame.time.wait(2500)
        make_new_game()
        Win = False


    pygame.display.update()