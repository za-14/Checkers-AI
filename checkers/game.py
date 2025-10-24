import pygame
from.constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, screen):
        self._temp()
        self.screen = screen

    def update(self):           #to update piece placement on board
        if self.screen is None:
          return
        self.board.draw(self.screen)   
        self.draw_valid_moves(self.valid_moves)     
        pygame.display.update()      
    
    def _temp(self):        #_init to _temp   priv
        self.selected = None        #selected piece
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}      #tells current valid moves dictionary of valid moves from any possible pos
    
    def winner(self):
        return self.board.winner()
    def reset(self):
        self._temp()
    
    def select(self, row, col):
       if self.selected:
           result = self._move(row,col)      #move selected piece to respective row & col using_move which ensuures move is valid and updates board pos 
           if not result:                     #if selected row/col (ie move) is not valid move
              self.selected = None           #reset selection
              self.select(row,col)           #reselect row, col 
       
       piece = self.board.get_piece(row,col)              #if 0  returned ie sq is empty else piece obj on sq is returned
       if piece != 0   and  piece.colour  == self.turn:   #if pos selected is not empty  and piece is as per curr player's turn
            self.selected = piece                            #then select that piece
            self.valid_moves = self.board.get_valid_moves(piece)       #pass that piece to valid moves funct
            return True                                               #valid piece slected
      
       return False

    def _move(self, row,col):       #priv
        piece = self.board.get_piece(row,col)                                 #chk selected row,col has RED/White piece or no piece
        if self.selected and piece == 0 and (row,col) in self.valid_moves:     #the selected piece being moved to an empty square, and that square is a valid move then proceed with the move.
            self.board.move(self.selected, row,col)                        #move curr selected piece to row col passed
            skipped = self.valid_moves[(row,col)]
            if skipped:
              self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True
    
    def draw_valid_moves(self,moves):
        if self.screen is None:
           return
        for move in moves:
            row ,col = move
            pygame.draw.circle(self.screen, BLUE, (col*SQUARE_SIZE+SQUARE_SIZE//2, row*SQUARE_SIZE+SQUARE_SIZE//2), 10)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board
    
    def check_no_moves(self, color):
        for piece in self.board.get_all_pieces(color):
          if self.board.get_valid_moves(piece):
            return False  # At least one piece has valid moves
        return True  # No moves available for this color


    def ai_move(self, board):
        self.board = board
        self.change_turn()

        
