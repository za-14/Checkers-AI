import pygame
from checkers.constants import WIDTH, HEIGHT, RED, WHITE
from checkers.game import Game
from reinforcement.algorithm3 import QLearningAgent
from copy import deepcopy
from minimax_prunned.algorithm2 import alpha_beta
import time  # Add this import at the top if it's not there


FPS = 60
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alpha-Beta (WHITE) vs Q-Learning (RED)")
clock = pygame.time.Clock()

def main():
    game = Game(SCREEN)
    agent = QLearningAgent(alpha=0.5, gamma=0.3)
    agent.load_q_table()  # Ensure qtable.pkl is in the correct path

    run = True
    while run:
        clock.tick(FPS)
        start_time = time.time()
        time_limit = 30 
        if game.turn == WHITE:
            _, new_board = alpha_beta(
            game.get_board(), depth=3, alpha=float('-inf'), beta=float('inf'),
            max_player=True, game=game, start_time=start_time, time_limit=time_limit
        )
            game.ai_move(new_board)

        elif game.turn == RED:
            state_key = agent.encode(game.get_board(), RED)
            valid_moves = agent.get_valid_actions(game.get_board(), RED)

            if not valid_moves:
                print("RED (Q Agent) has no valid moves. WHITE wins!")
                run = False
                continue

            piece, move = agent.choose_action(game.get_board(), state_key, valid_moves, RED)

            if piece is None or move is None:
                print("RED (Q Agent) failed to select a move.")
                run = False
                continue

            if not game.select(piece.row, piece.col):
                continue
            if not game._move(move[0], move[1]):
                continue


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if game.winner():
            print(f"{game.winner()} wins!")
            run = False

        if game.check_no_moves(game.turn):
            print(f"No moves left for {game.turn}")
            run = False

        game.update()

    pygame.quit()

if __name__ == "__main__":
    main()
