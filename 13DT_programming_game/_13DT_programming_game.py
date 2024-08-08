import pygame, sys, random
from pygame.math import Vector2

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

#classes
class LevelManager:
    def __init__(self):
        self.state = 'start_menu'
        
    def start_menu(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'instructions'
                
        screen.blit(start_bg, (0,0))

    def instructions(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, pygame.Color('red'), player_rect)
        pygame.draw.rect(screen, pygame.Color('blue'), landmark)
        
    def level_manager(self):
        if self.state == 'start_menu':
            self.start_menu()
        if self.state == 'instructions':
            self.instructions()

        
        collision_detection()
    
        pygame.display.update()
                
level_manager = LevelManager()

#objects 
player_rect = pygame.Rect(30, 30, 50, 50)
landmark = pygame.Rect(400, 400, 100, 100)

def player_movement(keys):
    #Receives a list of all key movements
    #Player 1
    vel = 1
    if keys[pygame.K_LEFT]:
        player_rect.x -= vel
    if keys[pygame.K_RIGHT]:
        player_rect.x += vel
    if keys[pygame.K_UP]:
        player_rect.y -= vel
    if keys[pygame.K_DOWN]:
        player_rect.y += vel
    #Player 2
    if keys[pygame.K_w]: #up
        player_rect.y -= vel
    if keys[pygame.K_s]: #down
        player_rect.y += vel
    if keys[pygame.K_a]: #left
        player_rect.x -= vel
    if keys[pygame.K_d]: #right
        player_rect.x += vel
      
def collision_detection():
    if player_rect.colliderect(landmark):
        print('collison')

#images ig?
start_bg = pygame.image.load("bookshelve.png")    
start_bg = pygame.transform.scale(start_bg, (800, 800))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pass

    keys = pygame.key.get_pressed()
    player_movement(keys)
    
    level_manager.level_manager()

    clock.tick(60)
