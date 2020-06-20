import numpy as np
import pygame
import sys

pygame.init()
# global variables
ROW_COUNT = 6
COLUMN_COUNT = 7
Blue = (0, 0, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Yellow = (255, 255, 0)

square_size = 100
width = COLUMN_COUNT * square_size
height = (ROW_COUNT + 1) * square_size
size = (width, height)
radius = int(square_size / 2 - 5)

screen = pygame.display.set_mode(size)


def create_board():
    board = np.zeros((6, 7))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[5][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, Blue, (c * square_size, r * square_size + square_size, square_size,
                                            square_size))  # (x cordinate, y cordinate , height , width)
            pygame.draw.circle(screen, Black, (
            int(c * square_size + square_size / 2), int(r * square_size + square_size + square_size / 2)), radius)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, Red, (
                    int(c * square_size + square_size / 2), int(height - r * square_size - square_size / 2)),
                                       radius)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, Yellow, (
                    int(c * square_size + square_size / 2), int(height - r * square_size - square_size / 2)),
                                       radius)

        pygame.display.update()


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal location for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True


board = create_board()
print_board(board)

game_over = False
turn = 0
draw_board(board)
myfont = pygame.font.SysFont("monospace", 75)
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0, 0, width, square_size))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, Red, (posx, int(square_size / 2)), radius)
            else:
                pygame.draw.circle(screen, Yellow, (posx, int(square_size / 2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, Black, (0, 0, width, square_size))

            # Ask for player 1
            if turn == 0:
                posx = event.pos[0]
                col = int(posx // square_size)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, Red)
                        screen.blit(label, (40, 10))  # update the specific part of the screen
                        game_over = True
            # Ask for player 2
            else:
                posx = event.pos[0]
                col = int(posx // square_size)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 1 wins!!", 1, Red)
                        screen.blit(label, (40, 10))  # update the specific part of the screen
                        game_over = True
            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2  # alternating between player 1 and 2 (0,1)
