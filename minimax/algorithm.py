#minimax
from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE):  # Removed game param
            evaluation = minimax(move, depth-1, False, game)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED):  # Removed game param
            evaluation = minimax(move, depth-1, True, game)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
        return minEval, best_move

def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

MAX_MOVES = 300  
def get_all_moves(board, color):  # Removed game param
    moves = []
    count = 0
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if count >= MAX_MOVES:
                return moves  # Exit early once max reached
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)
            count += 1
    return moves

# You can still use draw_moves() for player input visualization if needed
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.screen)
    pygame.draw.circle(game.screen, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100)
