# minimax with 30-second timeout
import pygame
import time
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(SCREEN)

    # Start the timer at the beginning
    game.board.reset_turn_timer()

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            board_size = len(game.get_board().board)
            depth = 3 if board_size == 8 else 2 if board_size == 16 else 1
            value, new_board = minimax(game.get_board(), depth, WHITE, game)
            game.ai_move(new_board)
            game.board.reset_turn_timer()  # Reset timer after AI move

        if game.winner() is not None:
            print("Winner:", game.winner())
            print("RED Captures:", game.board.red_captures)
            print("WHITE Captures:", game.board.white_captures)
            run = False

        if game.check_no_moves(game.turn):
            print(f"No moves left for {game.turn}.")
            winner = WHITE if game.turn == RED else RED
            print(f"{winner} wins!")
            print("RED Captures:", game.board.red_captures)
            print("WHITE Captures:", game.board.white_captures)
            run = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game exited by user.")
                print("RED Captures:", game.board.red_captures)
                print("WHITE Captures:", game.board.white_captures)
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == RED:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        # ⏱ Timeout check
        if game.turn == RED and game.board.turn_exceeded():
            print("⏰ RED took too long. Skipping turn.")
            game.change_turn()
            game.board.reset_turn_timer()

        game.update()

    pygame.quit()

main()
