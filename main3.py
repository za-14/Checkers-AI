import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
import time
from minimax_prunned.algorithm2 import alpha_beta

FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers Game')

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

       # AI turn (White)
        if game.turn == WHITE:
            start_time = time.time()
            time_limit = 2  # Set how long the AI is allowed to search (in seconds)
            value, new_board = alpha_beta(game.get_board(), 2, float('-inf'), float('inf'), True, game, start_time, time_limit)
            game.ai_move(new_board)
            game.board.reset_turn_timer()
        # Reset after AI move

        # Check for winner
        if game.winner() is not None:
            print("Winner:", game.winner())
            print("RED Captures:", game.board.red_captures)
            print("WHITE Captures:", game.board.white_captures)
            run = False

        # Check for no moves left
        elif game.check_no_moves(game.turn):
            print(f"No moves left for {game.turn}.")
            winner = WHITE if game.turn == RED else RED
            print(f"{winner} wins!")
            print("RED Captures:", game.board.red_captures)
            print("WHITE Captures:", game.board.white_captures)
            run = False
            continue

        # Event handling
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

        # Timeout check
        if game.turn == RED and game.board.turn_exceeded():
            print("⏰ RED took too long. Skipping turn.")
            game.change_turn()
            game.board.reset_turn_timer()

        game.update()

    pygame.quit()

main()
