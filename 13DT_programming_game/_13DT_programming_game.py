from stringprep import c22_specials
from tabnanny import check
from tkinter import HORIZONTAL
import pygame, sys
from maze_tilemaps_and_sprite_frames import player_surfaces_down, player_surfaces_left, player_surfaces_right, player_surfaces_up, maze1, maze2, maze3, empty_maze


pygame.init()
pygame.font.init()
base_font = pygame.font.Font('ErinsHandwriting-Regular.ttf',32)
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

#ASSETS & IMAGES
player_rect = player_surfaces_down[0].get_rect(topleft=(250, 250))

#map images
periodicals_room = pygame.image.load('periodicals_final1.png')
copy_room = pygame.image.load('copy_room_final2.png')
toilets_room = pygame.image.load('toilets_final.png')
childrens_room = pygame.image.load('childrens_final2.png')
study_room = pygame.image.load('studyroom_final.png')
nonfiction_room = pygame.image.load('nonfiction_final.png')
meeting_room = pygame.image.load('meetingroom_final.png')
map_menu = pygame.transform.scale(pygame.image.load('game_map.png'), (700, 500))
map_menu_rect = map_menu.get_rect()
inventory_menu = pygame.transform.scale(pygame.image.load('totebag.png'), (700, 700))
start_menu_surface = pygame.transform.scale(pygame.image.load('start_menu_2.png'), (800, 800))
instructions = pygame.transform.scale(pygame.image.load('instructions.png'), (800, 800))
vertical_door = pygame.transform.scale(pygame.image.load('vertical_door.png'), (10, 50))
horizontal_door = pygame.transform.scale(pygame.image.load('horizontal_door.png'), (50, 10))
#map_menu = pygame.transform.scale(map_menu, (1000, 600))

#door rects
#p_to_co_door 
#door0 = doors_group.append(pygame.Rect(350, 50, 50, 10))
#co_to_p_door a
#door1 = doors_group.append(pygame.Rect(420, 600, 50, 10))
#co_to_t_door 
#door2 = doors_group.append(pygame.Rect(580, 370, 10, 50))
#t_to_co_door 
#door3 = doors_group.append(pygame.Rect(185, 365, 10, 50))


#tile images
empty = pygame.transform.scale(pygame.image.load("empty_bordered.png"), (50, 50))  
#empty_rect = empty.get_rect()
bookshelf = pygame.transform.scale(pygame.image.load("bookshelve.png"), (50, 50))    
#bookshelf_rect = bookshelf.get_rect()
bookshelftop = pygame.transform.scale(pygame.image.load("bookshelftop.png"), (50, 50))   
#bookshelftop_rect = bookshelftop.get_rect()
wall = pygame.transform.scale(pygame.image.load("wall.png"), (50, 50)) 
#wall_rect = wall.get_rect()

TILE_SIZE = 50
tiles = [empty, bookshelf, bookshelftop, wall]
#tiles_rect = [empty_rect, bookshelf_rect, bookshelftop_rect, wall_rect]
tile_rects = []

solid_tile_indices = [1, 2, 3]
def draw_maze(maze):
    #print("start of def draw maze")
    #print(maze)
    #print("tile rects")
    #print(tile_rects)
    tile_rects.clear()
    #print("after clear")
    #print(tile_rects)
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))
            
            if maze[row][column] in solid_tile_indices:
                tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                tile_rects.append(tile_rect)

def menu_switching(next_level):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            level_manager.state = next_level
        #quit program
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    level_manager.state = 'map_menu'
                elif event.key == pygame.K_e:
                    level_manager.state = 'inventory_menu'

def level_labels(level_name, a, b, c):
    label = pygame.Rect(a, b, c, 30)
    pygame.draw.rect(screen, pygame.Color(92, 54, 88), label)    
    text = "{}".format(str(level_name))
    text_surface = base_font.render(text, True,(240, 232, 213))
    text_surface_rect = text_surface.get_rect(center = (screen_width/2, b+15))
    screen.blit(text_surface, text_surface_rect)
             
                
def wall_collision_detection(a, b, c, d):
    if player_rect.right >= a: 
        player.moving = False
        player_rect.right = a
    elif player_rect.left <= b:
        player.moving = False
        player_rect.left = b
    elif player_rect.top <= c:
        player.moving = False
        player_rect.top = c
    elif player_rect.bottom >= d:
        player.moving = False
        player_rect.bottom = d

bg_objects = []
        
def object_collision_detection():
    for obj in bg_objects:
        if player_rect.colliderect(obj):
            print('collision')
            return True
    return False

def tiles_collision_detection():
    if player_rect.collidelist(tile_rects) != -1:
        return True  # Collision detected
    return False
     
        
def check_for_doors(doors_group):
    for door in doors_group:
        #print (door)
        if player_rect.colliderect(door):
            print('collision')
            level_manager.state = door.destination
            doors_group = doors_group
    return doors_group

# position_resetted = False
    
# def reset_position(position_resetted, top_value, left_value):
#     if position_resetted == False:
#         player_rect.top = top_value
#         player_rect.left = left_value
#         position_resetted = True
#     return position_resetted

# def horizontal_tile_collision_detection():
#     if player_rect.midright.x >= tiles_rect[1:].midleft.x:
#         return True
#     elif player_rect.midleft.x <= tiles_rect[1:].midright.x:
#         return True
#     return False

# def vertical_tile_collision_detection():
#     if player_rect.midtop.y <= tiles_rect[1:].midbottom.y:
#         return True
#     elif player_rect.midbottom.y >= tiles_rect[1:].midtop.y:
#         return True
#     return False

class Player:
    def __init__(self, moving=False, value=0, direction='right', location='periodicals_level'):
        self.moving = moving
        self.value = value
        self.direction = direction
        self.location = location
        self.position_resetted = False
   
    def move_player(self, keys):
        vel = 10
        self.moving = False
        next_rect = player_rect.copy()
        # current_tile_x = player_rect.x // TILE_SIZE
        # current_tile_y = player_rect.y // TILE_SIZE
        # print(current_tile_x, current_tile_y)
      

        if keys[pygame.K_w]:# and current_tile_y > 0 and maze1[current_tile_y - 1][current_tile_x] == 0:
            next_rect.y -= vel#player_rect.y -= vel
            self.direction = 'up'
            self.moving = True
        elif keys[pygame.K_s]:# and current_tile_y < len(maze1) - 1 and maze1[current_tile_y + 1][current_tile_x] == 0:
            next_rect.y += vel#player_rect.y += vel
            self.direction = 'down'
            self.moving = True
        elif keys[pygame.K_a]:# and current_tile_x > 0 and maze1[current_tile_y][current_tile_x - 1] == 0:
            next_rect.x -= vel#player_rect.x -= vel
            self.direction = 'left'
            self.moving = True
        elif keys[pygame.K_d]:# and current_tile_x < len(maze1[0]) - 1 and maze1[current_tile_y][current_tile_x + 1] == 0:
            next_rect.x += vel#player_rect.x += vel
            self.direction = 'right'
            self.moving = True
        
        if next_rect.collidelist(tile_rects) == -1: #and not object_collision_detection():
            player_rect.update(next_rect)
        # if next_rect.collidelist(bg_objects) == -1:
        #     player_rect.update(next_rect)
        else:
            self.moving = False
            
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
        #pygame.draw.rect(screen, pygame.Color(0, 0, 0, a=0.1), player_rect) 

    def reset_position(self, top_value, left_value):
        if not self.position_resetted:
            player_rect.top = top_value
            player_rect.left = left_value
            if self.moving == True:
                self.position_resetted = True
        return self.position_resetted
            
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
CopyRoom = Room_List.append(Room((screen_width-300)/2, (screen_height-500)/2, 300, 500, copy_room,))
ToiletsRoom = Room_List.append(Room((screen_width-300)/2, (screen_width-300)/2, 300, 300, toilets_room))
ChildrensRoom = Room_List.append(Room((screen_width-700)/2, (screen_height-700)/2, 700, 700, childrens_room))
StudyRoom = Room_List.append(Room((screen_width-600)/2, (screen_height-500)/2, 600, 500, study_room))
NonfictonRoom = Room_List.append(Room((screen_width-500)/2, (screen_height-700)/2, 500, 700, nonfiction_room))
MeetingRoom = Room_List.append(Room((screen_width-500)/2, (screen_height-500)/2, 500, 500, meeting_room))


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, popup):
        pass
        
class Door(pygame.sprite.Sprite):
    def __init__(self, destination, image, x, y, width, height):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.destination = destination
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw_door(self):
        screen.blit(self.image, (self.x, self.y))

 
#doors_group = pygame.sprite.Group()
doors_group_periodicals = pygame.sprite.Group()
doors_group_copy = pygame.sprite.Group()
doors_group_toilets = pygame.sprite.Group()
doors_group_childrens = pygame.sprite.Group()
doors_group_study = pygame.sprite.Group()
doors_group_nonfiction = pygame.sprite.Group()
doors_group_meeting = pygame.sprite.Group()

door0 = Door('copy_level', horizontal_door, 250, 50, 50, 10)
door1 = Door('childrens_level', vertical_door, 640, 600, 10, 50)
door2 = Door('periodicals_level', horizontal_door, 350, 640, 50, 10)
door3 = Door('toilets_level', vertical_door, 540, 500, 10, 50)
door4 = Door('copy_level', vertical_door, 250, 450, 10, 50)
door5 = Door('periodicals_level', vertical_door, 50, 600, 10, 50) 
door6 = Door('study_level', horizontal_door, 350, 50, 100, 10)
door7 = Door('nonfiction_level', vertical_door, 740, 300, 10, 50)
door8 = Door('childrens_level', horizontal_door, 400, 640, 100, 10)
door9 = Door('childrens_level', vertical_door, 150, 300, 10, 50)
door10 = Door('meeting_level', horizontal_door, 400, 50, 10, 50)
door11 = Door('nonfiction_level', horizontal_door, 400, 640, 50, 10)
door12 = Door('end_menu', vertical_door, 640, 350, 100, 10)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = 'instructions_menu'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.blit(start_menu_surface, (0, 0))

    def instructions_menu(self):
        for event in pygame.event.get():
        #quit program
            if event.type == pygame.quit:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = 'periodicals_level'

        screen.blit(instructions, (0, 0))

    def periodicals_level(self):
        menu_switching('copy_level')
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state = 'copy_level'
       
        screen.fill((40, 25, 43)) 
        Room_List[0].draw_room()
        draw_maze(maze1)
        level_labels("Periodicals section", Room_List[0].x, Room_List[0].y+Room_List[0].height+10, Room_List[0].width)
        
        doors_group_periodicals.add(door0)
        doors_group_periodicals.add(door1)
        doors_group_periodicals.draw(screen)   

        computer1 = pygame.Rect(200, 130, 50, 60)  # Create the Rect object
        bg_objects.append(computer1)  # Append it to the list
        
        computer2 = pygame.Rect(300, 130, 50, 60)
        bg_objects.append(computer2)  # Append it to the list

        table1 = pygame.Rect(230, 350, 125, 125)
        bg_objects.append(table1)  # Append it to the list
        
        player.location = 'periodicals_level'
        position_resetted = False
        player.reset_position(150, 150)
        player.draw_player()
        player.move_player(keys)
        player.animate_player()

        check_for_doors(doors_group_periodicals)
        
        #pygame.draw.rect(screen, pygame.Color('brown'), p_to_co_door) 

        # if player_rect.colliderect(p_to_co_door):
        #     player_rect.x = co_to_p_door.x
        #     player_rect.y = co_to_p_door.y - 50
        #     self.state = 'copy_level'
 
        
    def copy_level(self):
        menu_switching('toilets_level')
        for event in pygame.event.get():
            #if event.type == keys[pygame.k_kp_enter]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                #self.state = 'toilets_level'   
                print(pygame.mouse.get_pos())     

        screen.fill((0, 0, 0)) 
        Room_List[1].draw_room()
        draw_maze(empty_maze)
        level_labels("Copy room", Room_List[1].x, Room_List[1].y+Room_List[1].height+10, Room_List[1].width)

        #doors_group[0].kill()
        
        doors_group_copy.add(door2)
        doors_group_copy.add(door3)
        doors_group_copy.draw(screen)  

        cabinet1 = pygame.Rect(255, 160, 165, 100)  # Create the Rect object
        bg_objects.append(cabinet1)  # Append it to the list
        
        drawers1 = pygame.Rect(425, 220, 125, 80)
        bg_objects.append(drawers1)  # Append it to the list
        
        copier = pygame.Rect(435, 325, 95, 120)
        bg_objects.append(copier)  # Append it to the list
       
        
        player.location = 'copy_level'
        #player.position_resetted = False
        player.draw_player()
        player.move_player(keys)
       
        #wall_collision_detection((Room_List[1].x+Room_List[1].width), (Room_List[1].x), (Room_List[1].y), (Room_List[1].y+Room_List[1].height))
        player.animate_player()

        check_for_doors(doors_group_copy)
        player.reset_position(400, 400)
        #pygame.draw.rect(screen, pygame.Color('brown'), co_to_p_door)
        #pygame.draw.rect(screen, pygame.Color('brown'), co_to_t_door)
        
        # if player_rect.colliderect(co_to_p_door):
        #     player_rect.x = p_to_co_door.x
        #     player_rect.y = p_to_co_door.y + 50
        #     self.state = 'periodicals_level'
        # elif player_rect.colliderect(co_to_t_door):
        #     player_rect.x = t_to_co_door.x + 50
        #     player_rect.y = t_to_co_door.y
        #     self.state = 'toilets_level'

    def toilets_level(self):
        menu_switching('childrens_level')        
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state =       

        screen.fill((0, 0, 0)) 
        Room_List[2].draw_room()
        draw_maze(empty_maze)
    
        doors_group_toilets.add(door4)
        doors_group_toilets.draw(screen)  
        
        toilets = pygame.Rect(260, 255, 155, 135)  # Create the Rect object
        bg_objects.append(toilets)  # Append it to the list
        
        cabinet2 = pygame.Rect(415, 255, 125, 80)
        bg_objects.append(cabinet2)  # Append it to the list
        
        sink = pygame.Rect(335, 490, 215, 60)
        bg_objects.append(sink)  # Append it to the list

        player.location = 'toilets_level'
        player.draw_player()
        player.move_player(keys)
        player.animate_player()
        #print(doors_group)
        check_for_doors(doors_group_toilets)
        #pygame.draw.rect(screen, pygame.Color('brown'), t_to_co_door)
        
        # if player_rect.colliderect(t_to_co_door):
        #     player_rect.x = co_to_t_door.x - 50
        #     player_rect.y = co_to_t_door.y
        #     self.state = 'copy_level'

    def childrens_level(self):
        menu_switching('study_level')        
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state =        
                
        screen.fill((0, 0, 0)) 
        Room_List[3].draw_room()
        draw_maze(maze2)
        
        doors_group_childrens.add(door5)
        doors_group_childrens.add(door6)
        doors_group_childrens.add(door7)
        doors_group_childrens.draw(screen)  
        
        
        player.location = 'childrens_level'
        player.draw_player()
        player.move_player(keys)
        player.animate_player() 
        
        check_for_doors(doors_group_childrens)
    
    def study_level(self):
        menu_switching('nonfiction_level')        
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state =      
                
        screen.fill((0, 0, 0)) 
        Room_List[4].draw_room()
        draw_maze(empty_maze)
        
        doors_group_study.add(door8)
        doors_group_study.draw(screen)  

        table2 = pygame.Rect(105, 155, 590, 130)  # Create the Rect object
        bg_objects.append(table2)  # Append it to the list  
        
        table3 = pygame.Rect(105, 285, 125, 360)
        bg_objects.append(table3)  # Append it to the list
        
        table4 = pygame.Rect(570, 285, 125, 360)
        bg_objects.append(table4)  # Append it to the list

        player.location = 'study_level'
        player.draw_player()
        player.move_player(keys)
        player.animate_player()

        check_for_doors(doors_group_study)
        print(door8.x, door8.y)
                
    def nonfiction_level(self):
        menu_switching('meeting_level')        
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state =       
                
        screen.fill((0, 0, 0)) 
        Room_List[5].draw_room()
        draw_maze(maze3)

        doors_group_nonfiction.add(door9)
        doors_group_nonfiction.add(door10)
        doors_group_nonfiction.add(door12)
        doors_group_nonfiction.draw(screen)  

        table5 = pygame.Rect(235, 130, 125, 125)
        bg_objects.append(table5)  # Append it to the list

        player.location = 'nonfiction_level'
        player.draw_player()
        player.move_player(keys)
        player.animate_player()

        check_for_doors(doors_group_nonfiction)


    def meeting_level(self):
        menu_switching('periodicals_level')
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state = 'meeting_level'   
                
        screen.fill((0, 0, 0)) 
        Room_List[6].draw_room()
        draw_maze(empty_maze)
        
        doors_group_meeting.add(door11)
        doors_group_meeting.draw(screen)
        
        table6 = pygame.Rect(265, 350, 280, 125)  # Create the Rect object
        bg_objects.append(table6)  # Append it to the list  # Draw the Rect 
        
        cabinet3 = pygame.Rect(260, 160, 70, 80)
        bg_objects.append(cabinet3)  # Append it to the list
        
        drawers3 = pygame.Rect(340, 195, 205, 75)
        bg_objects.append(drawers3)  # Append it to the list

        player.location = 'meeting_level'
        player.draw_player()
        player.move_player(keys)
        player.animate_player()

        check_for_doors(doors_group_meeting)
        
    def map_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_m:
                   self.state = player.location
        screen.fill((0, 0, 0))        
        screen.blit(map_menu, (50, 150))
        
    def inventory_menu(self):
        for event in pygame.event.get():
            #if event.type == keys[pygame.K_KP_ENTER]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.state = player.location  
        
        screen.fill((0, 0, 0))        
        screen.blit(inventory_menu, (50, 50))
  
    def level_manager(self):
        if self.state == 'start_menu':
            self.start_menu()
        if self.state == 'instructions_menu':
            self.instructions_menu()
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
        if self.state == 'meeting_level':
            self.meeting_level()
        if self.state == 'map_menu':
            self.map_menu()
        if self.state == 'inventory_menu':
            self.inventory_menu()
        pygame.display.update()       
                
level_manager = LevelManager()

while True:
   keys = pygame.key.get_pressed()
   level_manager.level_manager()
   clock.tick(60)
