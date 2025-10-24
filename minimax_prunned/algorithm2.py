import time
import random
import pickle
import os
import numpy as np
import pygame
from collections import defaultdict
from copy import deepcopy
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from checkers.board import Board
from checkers.piece import Piece


transposition_table = {}
MAX_MOVES = 300

def board_hash(board):
    pieces = []
    for row in board.board:
        for piece in row:
            if piece:
                pieces.append((piece.row, piece.col, piece.colour, piece.king))
    return tuple(sorted(pieces))


def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board, color):
    moves = []
    count = 0
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        ordered = sorted(valid_moves.items(), key=lambda x: len(x[1]), reverse=True)
        for move, skip in ordered:
            if count >= MAX_MOVES:
                return moves
            temp_board = board.clone()
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)
            count += 1
    return moves


def alpha_beta(position, depth, alpha, beta, max_player, game, start_time, time_limit):
    if time.time() - start_time > time_limit:
        return None, None
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    pos_hash = board_hash(position)
    if pos_hash in transposition_table:
        entry = transposition_table[pos_hash]
        return entry["value"], entry["move"]

    if max_player:
        max_eval = float('-inf')
        best_move = None
        moves = get_all_moves(position, WHITE)
        for move in moves:
            evaluation, _ = alpha_beta(move, depth - 1, alpha, beta, False, game, start_time, time_limit)
            if evaluation is None:
                return None, None
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break #prune
        transposition_table[pos_hash] = {"value": max_eval, "move": best_move}
        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        moves = get_all_moves(position, RED)
        for move in moves:
            evaluation, _ = alpha_beta(move, depth - 1, alpha, beta, True, game, start_time, time_limit)
            if evaluation is None:
                return None, None
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        transposition_table[pos_hash] = {"value": min_eval, "move": best_move}
        return min_eval, best_move

