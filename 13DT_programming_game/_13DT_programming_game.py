import pygame, sys, random
from pygame.math import Vector2

pygame.init()
cell_size = 4
cell_number = 200
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

#images & objects for now ig?
start_bg = pygame.image.load("bookshelve.png")    
start_bg = pygame.transform.scale(start_bg, (800, 800))
player_surface = pygame.image.load('earth.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (50, 50)) 
player_rect = player_surface.get_rect(center = (25, 25))
landmark = pygame.Rect(400, 400, 100, 100)
map_menu = pygame.image.load('game_map.png').convert_alpha()
map_menu = pygame.transform.scale(map_menu, (1000, 600))


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
            #if event.type == keys[pygame.K_KP_ENTER]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'
                
        screen.blit(start_bg, (0,0))

    def main_game(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = 'map_menu'

        screen.fill((175, 215, 70))                
        screen.blit(player_surface, player_rect)
        pygame.draw.rect(screen, pygame.Color('red'), landmark)
        self.collision_detection()
        
        
    def map_menu(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if event.type == keys[pygame.K_KP_ENTER]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = 'main_game'
                
        screen.blit(map_menu, (0,0))
        
    def collision_detection(self):
        if player_rect.colliderect(landmark):
            print('g')
            self.state = 'start_menu'
            player_rect.x = 20
  
    def level_manager(self):
        if self.state == 'start_menu':
            self.start_menu()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'map_menu':
            self.map_menu()

        player_movement(keys)
        pygame.display.update()
        
                
level_manager = LevelManager()

def player_movement(keys):
    #Receives a list of all key movements
    #Player 1
    vel = 3
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
      

while True:
    keys = pygame.key.get_pressed()

    level_manager.level_manager()

    clock.tick(60)
