import math
import sys
import numpy as np
import pygame

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    _board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return _board


def drop_piece(_board, _row, _col, _piece):
    board[_row][_col] = _piece


def is_valid_location(_board, _col):
    return _board[ROW_COUNT - 1][_col] == 0


def get_next_open_row(_board, _col):
    for r in range(ROW_COUNT):
        if _board[r][_col] == 0:
            return r


def print_board():
    print(np.flip(board, 0))


def winning_move(_board, _piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if _board[r][c] == _piece and _board[r][c + 1] == _piece and _board[r][c + 2] == _piece and \
                    _board[r][c + 3] == _piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if _board[r][c] == _piece and _board[r + 1][c] == _piece and _board[r + 2][c] == _piece and \
                    _board[r + 3][c] == _piece:
                return True

    # Check positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if _board[r][c] == _piece and _board[r + 1][c + 1] == _piece and _board[r + 2][c + 2] == _piece and \
                    _board[r + 3][c + 3] == _piece:
                return True

    # Check negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if _board[r][c] == _piece and _board[r - 1][c + 1] == _piece and _board[r - 2][c + 2] == _piece and \
                    _board[r - 3][c + 3] == _piece:
                return True


def draw_board(_board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, (0, 0, 255),
                             (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, (0, 0, 0), (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                   int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if _board[r][c] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                         height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
            elif _board[r][c] == 2:
                pygame.draw.circle(screen, (255, 255, 0), (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                           height - int(
                                                               r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
            pygame.display.update()


game_over = False
board = create_board()
turn = 0

pygame.init()

SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, (255, 0, 0), (posx, int(SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #  Ask for P1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARE_SIZE))
                        label = my_font.render("Player 1 WINS!!", 1, (255, 0, 0))
                        screen.blit(label, (40, 10))
                        game_over = True
            # Ask for P2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARE_SIZE))
                        label = my_font.render("Player 2 WINS!!", 1, (255, 255, 0))
                        screen.blit(label, (40, 10))
                        game_over = True

            draw_board(board)
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
