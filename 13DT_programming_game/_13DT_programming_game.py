import pygame, sys, random
from pygame.math import Vector2

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

player = pygame.Rect(50, 50, 100, 100)
landmark = pygame.Rect(50, 50, ,100, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pass


    screen.fill((175, 215, 70))
    pygame.display.update()
    clock.tick(60)
