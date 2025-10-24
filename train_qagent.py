# # Fixed Q-learning training loop for Checkers (Corrected for multiple episodes)

# import pygame
# import random
# from checkers.game import Game
# from checkers.constants import RED, WHITE
# from reinforcement.algorithm3 import QLearningAgent

# FPS = 60
# EPISODES = 10000 

# def training_model():
#     pygame.init()
#     screen = pygame.display.set_mode((1, 1))  # Dummy surface
#     clock = pygame.time.Clock()

#     agent = QLearningAgent(alpha=0.5, gamma=0.3)  

#     for episode in range(EPISODES):
#         game = Game(screen)
#         run = True
#         turn = WHITE  # WHITE = Q agent, RED = random

#         while run:
#             clock.tick(FPS)
#             state_key = agent.encode(game.get_board(), WHITE)

#             if turn == WHITE:
#                 valid_moves = agent.get_valid_actions(game.get_board(), WHITE)

#                 if not valid_moves:
#                     reward = -10
#                     agent.learn(state_key, None, reward, None, True)
#                     break

#                 piece, move = agent.choose_action(state_key, valid_moves, WHITE)

#                 if piece is None or move is None:
#                     reward = -15
#                     agent.learn(state_key, None, reward, None, True)
#                     run = False
#                     continue

#                 if not game.select(piece.row, piece.col):
#                     continue
#                 if not game._move(move[0], move[1]):
#                     continue

#                 skipped = game.get_board().get_valid_moves(piece).get(move)
#                 reward = 10 if skipped else -1

#                 next_state_key = agent.encode(game.get_board(), WHITE)
#                 done = game.winner() is not None

#                 agent.learn(state_key, (piece.row, piece.col, move[0], move[1]), reward, next_state_key, done)

#                 if game.winner() is not None:
#                     final_reward = 15 if game.winner() == WHITE else -10
#                     agent.learn(state_key, (piece.row, piece.col, move[0], move[1]), final_reward, None, True)
#                     run = False
#                     break

#                 turn = RED

#             else:
#                 pieces = game.get_board().get_all_pieces(WHITE)
#                 moves = []
#                 for piece in pieces:
#                     valid_moves = game.get_board().get_valid_moves(piece)
#                     for move in valid_moves:
#                         moves.append((piece, move))

#                 if not moves:
#                     break

#                 piece, move = random.choice(moves)
#                 game.select(piece.row, piece.col)
#                 game._move(move[0], move[1])
#                 turn = WHITE

#         # Epsilon decay after each episode
#         agent.epsilon = max(agent.epsilon * 0.995, 0.1)

#         print(f"Episode {episode} completed. Epsilon: {agent.epsilon:.3f}")

#     agent.save_q_table()
#     pygame.quit()

# if __name__ == "__main__":
#     training_model()
