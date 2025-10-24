import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from reinforcement.algorithm3 import QLearningAgent

FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers AI")

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    clock = pygame.time.Clock()
    game = Game(SCREEN)

    agent = QLearningAgent(alpha=0.5, gamma=0.3)
    agent.epsilon = 0  # deterministic
    if len(agent.q_table) == 0:
        print("Q-table is empty. Train the agent first.")
        return

    game.board.reset_turn_timer()

    run = True
    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            state = agent.encode(game.get_board(), WHITE)
            actions = agent.get_valid_actions(game.get_board(), WHITE)
            if actions:
                piece, move = agent.choose_action(game.get_board(), state, actions, WHITE)
                r1, c1 = piece.row, piece.col
                r2, c2 = move
                if game.select(r1, c1):
                    game._move(r2, c2)
            game.board.reset_turn_timer()

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

        if game.winner() is not None:
            print("Winner:", game.winner())
            print("RED Captures:", game.board.red_captures)
            print("WHITE Captures:", game.board.white_captures)
            run = False

        elif game.check_no_moves(game.turn):
            print(f"No moves left for {game.turn}.")
            winner = WHITE if game.turn == RED else RED
            print(f"{winner} wins!")
            print("RED Captures:", game.board.red_captures)
            print("WHITE Captures:", game.board.white_captures)
            run = False

        elif game.turn == RED and game.board.turn_exceeded():
            print("⏰ RED took too long. Skipping turn.")
            game.change_turn()
            game.board.reset_turn_timer()

        game.update()

    pygame.quit()

if __name__ == "__main__":
    main()
