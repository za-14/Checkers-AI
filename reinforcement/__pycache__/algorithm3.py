import random
import pickle
import os
import numpy as np
from checkers.board import Board
from checkers.game import Game
from checkers.piece import Piece

RED = (255, 0, 0)
WHITE = (255, 255, 255)

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_decay=0.999, epsilon_min=0.05, load_file="qtable.pkl"):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.load_file = load_file
        self.load_q_table()
        self.player_color = WHITE
        self.opponent_color = RED

    def get_q_value(self, state_key, action):
        return self.q_table.get((state_key, action), 0.0)

    def choose_action(self, state_key, valid_moves, color):
        if not valid_moves:
            return None, None

        if random.random() < self.epsilon:
            return random.choice(valid_moves)

        q_values = [
            (self.get_q_value(state_key, self.action_to_key(pos, move)), (pos, move)) 
            for pos, move in valid_moves
        ]

        if not q_values:
            return random.choice(valid_moves)

        max_q = max(q_values, key=lambda x: x[0])[0]
        best_actions = [action for q, action in q_values if q == max_q]

        # Prefer capturing moves among best actions
        for action in best_actions:
            piece, move = action
            moves = Board.get_valid_moves(piece)
            if move in moves and moves[move]:  # skipped pieces exist
                return action

        return random.choice(best_actions)

    def learn(self, old_state_key, action, reward, next_state_key, done):
        old_q = self.get_q_value(old_state_key, action)
        future_q = 0 if done else max(
            [self.get_q_value(next_state_key, a) for a in self.possible_actions(next_state_key)], default=0
        )

        new_q = old_q + self.alpha * (reward + self.gamma * future_q - old_q)
        self.q_table[(old_state_key, action)] = new_q

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    def choose_action(self, board, state_key, valid_moves, color):
        if not valid_moves:
            return None, None

        if random.random() < self.epsilon:
            return random.choice(valid_moves)

        q_values = [
            (self.get_q_value(state_key, self.action_to_key(pos, move)), (pos, move)) 
            for pos, move in valid_moves
        ]

        if not q_values:
            return random.choice(valid_moves)

        max_q = max(q_values, key=lambda x: x[0])[0]
        best_actions = [action for q, action in q_values if q == max_q]

        # Prefer capturing moves among best actions
        for action in best_actions:
            piece, move = action
            moves = board.get_valid_moves(piece)
            if move in moves and moves[move]:  # move exists and captures
                return action

        return random.choice(best_actions)

    def action_to_key(self, piece_pos, move):
        return (piece_pos, move)

    def possible_actions(self, state_key):
        return [action for s, action in self.q_table.keys() if s == state_key]

    def save_q_table(self):
        with open(self.load_file, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self):
        if os.path.exists(self.load_file):
            with open(self.load_file, "rb") as f:
                self.q_table = pickle.load(f)

    def train(self, episodes=1000):
        for episode in range(episodes):
            game = Game(None)
            board = game.get_board()
            done = False
            move_count = 0
            max_moves = 200

            while not done and move_count < max_moves:
                state = self.encode(board, self.player_color)
                valid_actions = self.get_valid_actions(board, self.player_color)
                piece, move = self.choose_action(state, valid_actions, self.player_color)

                if piece is None or move is None:
                    reward = -1
                    done = True
                    continue

                prev_score = board.evaluate(self.player_color)
                skipped = board.get_valid_moves(piece)[move]
                board.move(piece, move[0], move[1])
                if skipped:
                    board.remove(skipped)

                if board.winner() is not None or game.check_no_moves(self.opponent_color):
                    reward = 1
                    done = True
                else:
                    reward = board.evaluate(self.player_color) - prev_score

                next_state = self.encode(board, self.player_color)
                self.learn(state, (piece.row, piece.col, move[0], move[1]), reward, next_state, done)

                game.change_turn()
                move_count += 1

            if episode % 100 == 0:
                print(f"Episode {episode} completed. Epsilon: {self.epsilon:.3f}")

            self.epsilon *= self.epsilon_decay
            self.save_q_table()

    def encode(self, board, color):
        encoded = []
        for row in board.board:
            for piece in row:
                if piece is None or not hasattr(piece, 'colour'):
                    encoded.append(0)
                else:
                    val = 1 if piece.colour == WHITE else -1
                    if piece.king:
                        val *= 2
                    encoded.append(val)
        return tuple(encoded + [1 if color == WHITE else -1])

    def get_valid_actions(self, board, color):
        actions = []
        capture_actions = []

        pieces = board.get_all_pieces(color)
        for piece in pieces:
            moves = board.get_valid_moves(piece)
            for move, skipped in moves.items():
                action = (piece, move)
                if skipped:
                    capture_actions.append(action)
                else:
                    actions.append(action)

        return capture_actions if capture_actions else actions
