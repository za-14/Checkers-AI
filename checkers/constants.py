import pygame

WIDTH = 500
HEIGHT = 500
ROWS = 16
COLS = 16
SQUARE_SIZE = WIDTH//COLS  #size of each checker board square

RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
BEIGE = (216,163,91)
BROWN = (155,91,18)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown2.png'),(44,25))      # 44,25 = resolution
