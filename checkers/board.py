import pygame
import time
from .constants import ROWS, WHITE, SQUARE_SIZE, COLS, BLACK, RED
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 32
        self.red_king = self.white_king = 0
        self.red_captures = 0
        self.white_captures = 0
        self.turn_start_time = time.time()
        self.create_board()

    def draw_sq(self, screen):
        screen.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(screen, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_king * 0.5 - self.red_king * 0.5)

    def get_all_pieces(self, colour):
        return [piece for row in self.board for piece in row if piece != 0 and piece.colour == colour]

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # King only if piece is on opponent's baseline AND has captured >= 2 enemy pieces
        if ((piece.colour == WHITE and row == ROWS - 1) or
            (piece.colour == RED and row == 0)) and piece.capture_count >= 2:
            if not piece.king:
                piece.make_king()
                if piece.colour == WHITE:
                    self.white_king += 1
                else:
                    self.red_king += 1


    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 6:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 9:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, screen):
        self.draw_sq(screen)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.colour == RED:
                self.red_left -= 1
                self.white_captures += 1
            else:
                self.white_left -= 1
                self.red_captures += 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

    def get_valid_moves(self, piece):
        moves = {}
        max_range = 4 if piece.king else 2

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            for i in range(1, max_range):
                mid_r = piece.row + dr * i
                mid_c = piece.col + dc * i
                end_r = piece.row + dr * (i + 1)
                end_c = piece.col + dc * (i + 1)

                if not (0 <= mid_r < ROWS and 0 <= mid_c < COLS and 0 <= end_r < ROWS and 0 <= end_c < COLS):
                    break

                mid_piece = self.board[mid_r][mid_c]
                end_piece = self.board[end_r][end_c]

                if isinstance(mid_piece, Piece) and mid_piece.colour != piece.colour and end_piece == 0:
                    moves[(end_r, end_c)] = [mid_piece]
                    break

        if not moves:
            for dr, dc in directions:
                for i in range(1, max_range + 1):
                    row = piece.row + dr * i
                    col = piece.col + dc * i
                    if 0 <= row < ROWS and 0 <= col < COLS and self.board[row][col] == 0:
                        moves[(row, col)] = []
                    else:
                        break

        return moves

    def reset_turn_timer(self):
        self.turn_start_time = time.time()

    def turn_exceeded(self):
        return time.time() - self.turn_start_time > 30

    def get_capture_counts(self):
        return self.red_captures, self.white_captures
    
    def clone(self):
        new_board = Board()
        new_board.board = []

        for row in self.board:
            new_row = []
            for piece in row:
                if piece == 0:
                    new_row.append(0)
                else:
                    # Create a new Piece with same attributes
                    new_piece = Piece(piece.row, piece.col, piece.colour)
                    new_piece.king = piece.king
                    new_piece.capture_count = piece.capture_count
                    new_row.append(new_piece)
            new_board.board.append(new_row)

        # Copy other attributes
        new_board.red_left = self.red_left
        new_board.white_left = self.white_left
        new_board.red_king = self.red_king
        new_board.white_king = self.white_king
        new_board.red_captures = self.red_captures
        new_board.white_captures = self.white_captures
        new_board.turn_start_time = self.turn_start_time

        return new_board

