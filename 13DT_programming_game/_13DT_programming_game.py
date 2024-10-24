from collections import defaultdict
import pygame, sys, random
from pygame.math import Vector2

pygame.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)


#images & objects for now ig?
start_bg = pygame.image.load("bookshelve.png")    
start_bg = pygame.transform.scale(start_bg, (900, 800))

player_surfaces = [
    pygame.transform.scale(pygame.image.load('real_assets/B1.png'), (30, 50)),
    pygame.transform.scale(pygame.image.load('real_assets/B2.png'), (30, 50)),
    pygame.transform.scale(pygame.image.load('real_assets/B3.png'), (30, 50)),
    pygame.transform.scale(pygame.image.load('real_assets/B4.png'), (30, 50))
]
player_rect = player_surfaces[0].get_rect()
   

map_menu = pygame.image.load('game_map.png').convert_alpha()
map_menu = pygame.transform.scale(map_menu, (1000, 600))

copy_room = pygame.image.load('copy_room.png')
periodicals_room = pygame.image.load('periodicals_final1.png')
toilets_room = pygame.image.load('toilets_room.png')

p_to_co_door = pygame.Rect(340, 50, 100, 10)
co_to_p_door = pygame.Rect(420, 680, 100, 10)
co_to_t_door = pygame.Rect(580, 370, 10, 100)
t_to_co_door = pygame.Rect(185, 365, 10, 100)

value = 0

class Player:
    def __init__(self, moving=False, value=0):
        self.moving = moving
        self.value = value
   

    def move_player(self, keys):
        vel = 5
        self.moving = False
        if keys[pygame.K_w]: #up
            player_rect.y -= vel
        if keys[pygame.K_s]: #down
            player_rect.y += vel
            self.moving = True
        if keys[pygame.K_a]: #left
            player_rect.x -= vel
        if keys[pygame.K_d]: #right
            player_rect.x += vel
            
    def animate_player(self):
        if self.moving:
            self.value += 1
            if self.value >= len(player_surfaces):
                self.value = 0
    def draw_player(self):
        screen.blit(player_surfaces[self.value], player_rect)
        #pygame.draw.rect(screen, pygame.Color('black'), player_rect) 
            
            
player = Player()   

class Room:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        
    def draw_room(self):
        global draw_room
        screen.blit(self.image, (self.x, self.y))
        #self.width = width
        #self.height = height
        #for room in room_list:
            #room_surface = pygame.transform.scale(room, (width, height))
            #room_rect = room_surface.get_rect()
            #screen.blit(room_surface, room_rect)   

Room_List = []        

PeriodicalsRoom = Room_List.append(Room((screen_width-500)/2, (screen_height-700)/2, 500, 700, periodicals_room))
CopyRoom = Room_List.append(Room(200, 100, 400, 600, copy_room))
ToiletsRoom = Room_List.append(Room(150, 100, 500, 600, toilets_room))


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
                self.state = 'periodicals_level'
                
        screen.blit(start_bg, (0,0))


    def periodicals_level(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = 'map_menu'
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        screen.fill((0, 0, 0)) 
        Room_List[0].draw_room()
        player.draw_player()
        player.move_player(keys)
        player.animate_player()
        pygame.draw.rect(screen, pygame.Color('brown'), p_to_co_door) 
        
        if player_rect.colliderect(p_to_co_door):
            player_rect.x = co_to_p_door.x
            player_rect.y = co_to_p_door.y - 50
            self.state = 'copy_level'
         
    def copy_level(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = 'map_menu'
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        screen.fill((102, 54, 81)) 
        Room_List[1].draw_room()
        pygame.draw.rect(screen, pygame.Color('brown'), co_to_p_door)
        pygame.draw.rect(screen, pygame.Color('brown'), co_to_t_door)
        
        if player_rect.colliderect(co_to_p_door):
            player_rect.x = p_to_co_door.x
            player_rect.y = p_to_co_door.y + 50
            self.state = 'periodicals_level'
        elif player_rect.colliderect(co_to_t_door):
            player_rect.x = t_to_co_door.x + 50
            player_rect.y = t_to_co_door.y
            self.state = 'toilets_level'

    def toilets_level(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = 'map_menu'
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        screen.fill((0, 0, 0)) 
        Room_List[2].draw_room()
        Player.draw_player(self)
        pygame.draw.rect(screen, pygame.Color('brown'), t_to_co_door)
        
        if player_rect.colliderect(t_to_co_door):
            player_rect.x = co_to_t_door.x - 50
            player_rect.y = co_to_t_door.y
            self.state = 'copy_level'

        
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())       
                
        screen.blit(map_menu, (0,0))
        
  
    def level_manager(self):
        if self.state == 'start_menu':
            self.start_menu()
        if self.state == 'periodicals_level':
            self.periodicals_level()
        if self.state == 'copy_level':
            self.copy_level()
        if self.state == 'toilets_level':
            self.toilets_level()
        if self.state == 'map_menu':
            self.map_menu()


        pygame.display.update()
        
                
level_manager = LevelManager()

while True:
    keys = pygame.key.get_pressed()
    level_manager.level_manager()
    clock.tick(12)
