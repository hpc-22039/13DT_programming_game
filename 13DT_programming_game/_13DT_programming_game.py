import pygame, sys
from maze_tilemaps_and_sprite_frames import player_surfaces_down, player_surfaces_left, player_surfaces_right, player_surfaces_up, maze1, maze2, maze3


pygame.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

#ASSETS & IMAGES
player_rect = player_surfaces_down[0].get_rect(topleft=(150, 150))


map_menu = pygame.image.load('game_map.png').convert_alpha()
map_menu = pygame.transform.scale(map_menu, (1000, 600))

#map images
periodicals_room = pygame.image.load('periodicals_final1.png')
copy_room = pygame.image.load('copyroom_final.png')
toilets_room = pygame.image.load('toilets_final.png')
childrens_room = pygame.image.load('childrens_final2.png')
study_room = pygame.image.load('studyroom_final.png')
nonfiction_room = pygame.image.load('nonfiction_final.png')
meeting_room = pygame.image.load('meetingroom_final.png')

#door rects
p_to_co_door = pygame.Rect(350, 50, 50, 10)
co_to_p_door = pygame.Rect(420, 600, 50, 10)
co_to_t_door = pygame.Rect(580, 370, 10, 50)
t_to_co_door = pygame.Rect(185, 365, 10, 50)

#tile images
empty = pygame.transform.scale(pygame.image.load("empty.png"), (50, 50))  
bookshelf = pygame.transform.scale(pygame.image.load("bookshelve.png"), (50, 50))    
bookshelftop = pygame.transform.scale(pygame.image.load("bookshelftop.png"), (50, 50))   
wall = pygame.transform.scale(pygame.image.load("wall.png"), (50, 50)) 

TILE_SIZE = 50
tiles = [empty, bookshelf, bookshelftop, wall]

def draw_maze(maze):
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))


class Player:
    def __init__(self, moving=False, value=0, direction='right', location='periodicals_level'):
        self.moving = moving
        self.value = value
        self.direction = direction
        self.location = location
   
    def move_player(self, keys):
        vel = 3
        self.moving = False
        current_tile_x = player_rect.x // TILE_SIZE
        current_tile_y = player_rect.y // TILE_SIZE
        print(current_tile_x, current_tile_y)
        if keys[pygame.K_w] and current_tile_y > 0 and maze1[current_tile_y - 1][current_tile_x] == 0:
            player_rect.y -= vel
            self.direction = 'up'
            self.moving = True
        elif keys[pygame.K_s] and current_tile_y < len(maze1) - 1 and maze1[current_tile_y + 1][current_tile_x] == 0:
            player_rect.y += vel
            self.direction = 'down'
            self.moving = True
        elif keys[pygame.K_a] and current_tile_x > 0 and maze1[current_tile_y][current_tile_x - 1] == 0:
            player_rect.x -= vel
            self.direction = 'left'
            self.moving = True
        elif keys[pygame.K_d] and current_tile_x < len(maze1[0]) - 1 and maze1[current_tile_y][current_tile_x + 1] == 0:
            self.direction = 'right'
            player_rect.x += vel
            self.moving = True

            
    def animate_player(self):
        if self.moving:
            self.value += 0.2 #incrementing the surface lists index
            if self.value >= len(player_surfaces_down):
                self.value = 0

    def draw_player(self):
        if self.direction == 'down':
            if self.moving == False:
                screen.blit(player_surfaces_down[0], player_rect) #idle frame
            else:
                screen.blit(player_surfaces_down[int(self.value)], player_rect) #
        elif self.direction == 'up':
            if self.moving == False:
                screen.blit(player_surfaces_up[0], player_rect)
            else:
                screen.blit(player_surfaces_up[int(self.value)], player_rect)
        elif self.direction == 'left':
            if self.moving == False:
                screen.blit(player_surfaces_left[0], player_rect)
            else:
                screen.blit(player_surfaces_left[int(self.value)], player_rect)
        elif self.direction == 'right':
            if self.moving == False:
                screen.blit(player_surfaces_right[0], player_rect)
            else:             
                screen.blit(player_surfaces_right[int(self.value)], player_rect)
        pygame.draw.rect(screen, pygame.Color(0, 0, 0, a=0.1), player_rect) 

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
        #global draw_room
        screen.blit(self.image, (self.x, self.y))
        #self.width = width
        #self.height = height
        #for room in room_list:
            #room_surface = pygame.transform.scale(room, (width, height))
            #room_rect = room_surface.get_rect()
            #screen.blit(room_surface, room_rect)          

Room_List = []        

PeriodicalsRoom = Room_List.append(Room((screen_width-500)/2, (screen_height-700)/2, 500, 700, periodicals_room))
CopyRoom = Room_List.append(Room((screen_width-300)/2, (screen_height-500)/2, 300, 500, copy_room))
ToiletsRoom = Room_List.append(Room((screen_width-300)/2, (screen_width-300)/2, 300, 300, toilets_room))
ChildrensRoom = Room_List.append(Room((screen_width-700)/2, (screen_height-700)/2, 700, 700, childrens_room))
StudyRoom = Room_List.append(Room((screen_width-600)/2, (screen_height-500)/2, 600, 500, study_room))
NonfictonRoom = Room_List.append(Room((screen_width-500)/2, (screen_height-700)/2, 500, 700, nonfiction_room))
MeetingRoom = Room_List.append(Room((screen_width-500)/2, (screen_height-700)/2, 500, 500, meeting_room))

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, popup):
        pass
        

        

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
        draw_maze(maze1)
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

        screen.fill((0, 0, 0)) 
        Room_List[1].draw_room()
        player.draw_player()
        player.move_player(keys)
        player.animate_player()
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
                self.state = 'childrens_level'

        screen.fill((0, 0, 0)) 
        Room_List[2].draw_room()
        player.draw_player()
        player.move_player(keys)
        player.animate_player()
        pygame.draw.rect(screen, pygame.Color('brown'), t_to_co_door)
        
        if player_rect.colliderect(t_to_co_door):
            player_rect.x = co_to_t_door.x - 50
            player_rect.y = co_to_t_door.y
            self.state = 'copy_level'

    def childrens_level(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if event.type == keys[pygame.K_KP_ENTER]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'nonfiction_level'
                
        screen.fill((0, 0, 0)) 
        Room_List[3].draw_room()
        draw_maze(maze2)
        player.draw_player()
        player.move_player(keys)
        player.animate_player() 
    
    def study_level(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if event.type == keys[pygame.K_KP_ENTER]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'nonfiction_level'
                
        screen.fill((0, 0, 0)) 
        Room_List[4].draw_room()
        player.draw_player()
        player.move_player(keys)
        player.animate_player()
                
    def nonfiction_level(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if event.type == keys[pygame.K_KP_ENTER]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'periodicals_level'
                
        screen.fill((0, 0, 0)) 
        Room_List[5].draw_room()
        draw_maze(maze3)
        player.draw_player()
        player.move_player(keys)
        player.animate_player()
        
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
        if self.state == 'childrens_level':
            self.childrens_level()
        if self.state == 'study_level':
            self.study_level()
        if self.state == 'nonfiction_level':
            self.nonfiction_level()
        if self.state == 'map_menu':
            self.map_menu()



        pygame.display.update()
        
                
level_manager = LevelManager()

while True:
   keys = pygame.key.get_pressed()
   level_manager.level_manager()
   clock.tick(60)
