import sys
import pygame
import math
import random
import numpy as np


class Level:
    def __init__(self, rows=3, cols=4):
        self.rows = rows
        self.cols = cols

    def setrows(self, rows):
        self.rows = rows

    def getrows(self):
        return self.rows

    def setcols(self, cols):
        self.cols = cols

    def getcols(self):
        return self.cols


class Card:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos


def change_level(num):
    if num == 1:
        lvl.setrows(3)
        lvl.setcols(4)
    elif num == 2:
        lvl.setrows(4)
        lvl.setcols(4)
    elif num == 3:
        lvl.setrows(4)
        lvl.setcols(5)


def values(num):
    if num == 1:
        _card_values = [1, 2, 3, 4, 5, 6]
    elif num == 2:
        _card_values = [1, 2, 3, 4, 5, 6, 7, 8]
    elif num == 3:
        _card_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return _card_values


def create_board(_lvl):
    _board = np.zeros((_lvl.getrows(), _lvl.getcols()))
    return _board


def choose_card(_board, _col, _row):
    return Card(_board[_row][_col], [_row, _col])


def place_cards(_board, _cards):
    occupied = [[-1, -1]]
    i = 0
    col = -1
    row = -1
    for card in _cards:
        while [row, col] in occupied:
            col = random.randrange(0, lvl.getcols())
            row = random.randrange(0, lvl.getrows())
        occupied.append([row, col])
        _board[row][col] = card


def reveal_card(_card):
    for c in range(lvl.getcols()):
        for r in range(lvl.getrows()):
            if [r, c] == _card.pos:
                rect = pygame.draw.rect(screen, (255, 255, 0), (int(c * SQUARE_SIZE + SQUARE_SIZE / 4),
                                                                int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 4),
                                                                int(SQUARE_SIZE / 2 + 10), int(SQUARE_SIZE / 2 + 30)))
                val_text = font_obj.render(str(int(_card.value)), True, (0, 0, 255))
                rect_text = val_text.get_rect(center=rect.center)
                screen.blit(val_text, rect_text)
            pygame.display.update()


def hide_card(_card):
    for c in range(lvl.getcols()):
        for r in range(lvl.getrows()):
            if [r, c] == _card.pos:
                pygame.draw.rect(screen, (255, 0, 0), (int(c * SQUARE_SIZE + SQUARE_SIZE / 4),
                                                       int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 4),
                                                       int(SQUARE_SIZE / 2 + 10), int(SQUARE_SIZE / 2 + 30)))
            pygame.display.update()


def draw_board(_board):
    for c in range(lvl.getcols()):
        for r in range(lvl.getrows()):
            pygame.draw.rect(screen, (0, 0, 0),
                             (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, (255, 0, 0), (int(c * SQUARE_SIZE + SQUARE_SIZE / 4),
                                                   int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 4),
                                                   int(SQUARE_SIZE / 2 + 10), int(SQUARE_SIZE / 2 + 30)))
            pygame.display.update()


win = False
card_values = values(2)
card_values = card_values * 2
lvl = Level()
change_level(2)
board = create_board(lvl)
place_cards(board, card_values)
print(board)
pygame.init()

SQUARE_SIZE = 100
width = lvl.getcols() * SQUARE_SIZE
height = (lvl.getrows() + 1) * SQUARE_SIZE
size = (width, (height + int(SQUARE_SIZE / 2)))

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
font_obj = pygame.font.Font('freesansbold.ttf', 20)

revealed = []
pick = 0


def check_win():
    if len(revealed) == int(len(card_values) / 2):
        print("Congrats, game won!!")
        pygame.time.wait(3000)
        return True
    else:
        return False


while not win:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        win = check_win()
        if win:
            exit(1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            col = int(math.floor(event.pos[0] / SQUARE_SIZE))
            row = int(math.floor(event.pos[1] / SQUARE_SIZE)) - 1
            print(row, col)
            if pick == 0:
                print("picking card 1")
                card1 = choose_card(board, col, row)
                if card1.value in revealed:
                    continue
                reveal_card(card1)
                pick = pick + 1
            else:
                if [row, col] == card1.pos:
                    print("Already picked")
                    continue
                else:
                    print("picking card 2")
                    card2 = choose_card(board, col, row)
                    if card2.value in revealed:
                        continue
                    reveal_card(card2)
                    if card2.value == card1.value and card1.value not in revealed:
                        print("nice found pair")
                        revealed.append(int(card1.value))
                        print(revealed)
                        pick = 0
                    else:
                        pygame.time.wait(500)
                        hide_card(card1)
                        hide_card(card2)
                        card1 = None
                        card2 = None
                        pick = 0
