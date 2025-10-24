# 2 player
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED
from checkers.game import Game

#WIDTH = 500
#HEIGHT = 500

#pygame.init()
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH , HEIGHT))   # WIN == SCREEN
pygame.display.set_caption('Checkers Game')

def get_rowcol_from_mouse(pos):     #based on mouse pos tells row & col
    x, y = pos
    row = y // SQUARE_SIZE
    col = x// SQUARE_SIZE
    return row,col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(SCREEN)     #game obj

    while run:
        clock.tick(FPS)
        if game.winner() != None:
            print(game.winner())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:      #if user hits quit button
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_rowcol_from_mouse(pos)
                #if game.turn == RED:
                game.select(row,col)
        game.update()
    
    pygame.quit() 


main()   