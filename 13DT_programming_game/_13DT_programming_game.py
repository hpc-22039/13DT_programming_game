import pygame, sys
from maze_tilemaps_and_sprite_frames import player_surfaces_down, player_surfaces_left, player_surfaces_right, player_surfaces_up, maze1, maze2, maze3, empty_maze

pygame.init()
pygame.font.init()
base_font = pygame.font.Font('ErinsHandwriting-Regular.ttf',32)
#setting up the screen and its dimensions, clock
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

#ASSETS & IMAGES
#room images
periodicals_room = pygame.image.load('periodicals_final1.png')
copy_room = pygame.image.load('copy_room_final2.png')
toilets_room = pygame.image.load('toilets_final.png')
childrens_room = pygame.image.load('childrens_final2.png')
study_room = pygame.image.load('studyroom_final.png')
nonfiction_room = pygame.image.load('nonfiction_final.png')
meeting_room = pygame.image.load('meetingroom_final.png')

#menu images
map_menu = pygame.transform.scale(pygame.image.load('game_map.png'), (700, 500))
map_menu_rect = map_menu.get_rect()
inventory_menu = pygame.transform.scale(pygame.image.load('totebag.png'), (700, 700))
start_menu_surface = pygame.transform.scale(pygame.image.load('start_menu_2.png'), (800, 800))
instructions = pygame.transform.scale(pygame.image.load('instructions.png'), (800, 800))

#door and item images
vertical_door = pygame.transform.scale(pygame.image.load('vertical_door.png'), (10, 50))
horizontal_door = pygame.transform.scale(pygame.image.load('horizontal_door.png'), (50, 10))

#door rects
p_to_co_door = pygame.Rect(350, 50, 50, 10)
co_to_p_door = pygame.Rect(350, 640, 50, 10)
co_to_t_door = pygame.Rect(540, 500, 10, 50) 
t_to_co_door = pygame.Rect(185, 365, 10, 50)

#tile images
empty = pygame.transform.scale(pygame.image.load("empty.png"), (50, 50))  
#empty_rect = empty.get_rect()
bookshelf = pygame.transform.scale(pygame.image.load("bookshelve.png"), (50, 50))    
#bookshelf_rect = bookshelf.get_rect()
bookshelftop = pygame.transform.scale(pygame.image.load("bookshelftop.png"), (50, 50))   
#bookshelftop_rect = bookshelftop.get_rect()
wall = pygame.transform.scale(pygame.image.load("wall.png"), (50, 50)) 
#wall_rect = wall.get_rect()

TILE_SIZE = 50 #size of square tiles for tilemaps
tiles = [empty, bookshelf, bookshelftop, wall] #a list of tiles surfaces used
tile_rects = [] #a list of tile rects used for collision detection
#tiles_rect = [empty_rect, bookshelf_rect, bookshelftop_rect, wall_rect]
solid_tile_indices = [1, 2, 3] #indices of occupied tiles

#function used to draw maze tilemaps
def draw_maze(maze): #maze lists are passed in to draw them 
    #print("start of def draw maze")
    #print(maze)
    #print("tile rects")
    #print(tile_rects)
    tile_rects.clear() 
    #print("after clear")
    #print(tile_rects)
    for row in range(len(maze)): #looping through range of each 'row' or list element in overall list
        for column in range(len(maze[row])): #looping through each element in inside of each 'row'/list element
            x = column * TILE_SIZE #setting width of tilemap as tile size times column
            y = row * TILE_SIZE #setting height of tilemap as tile size times row
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))
            
            #getting rects of occupied tiles & adding them to tile rects list for collision detection
            if maze[row][column] in solid_tile_indices: 
                tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                tile_rects.append(tile_rect)

#function used to handle exiting & switching into map & inventory menu within each room/level
def menu_switching(next_level): 
    for event in pygame.event.get(): #using pygame events to handle user input
        if event.type == pygame.MOUSEBUTTONDOWN:
            level_manager.state = next_level
        if event.type == pygame.QUIT: ##quit program if cross is clicked
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN: #switching into map if m key is pressed
                if event.key == pygame.K_m:
                    level_manager.state = 'map_menu'
                elif event.key == pygame.K_e: #switching into inventory is e key is pressed
                    level_manager.state = 'inventory_menu'

#function used to draw/blit labels to name each level 
def level_labels(level_name, a, b, c): #level name, & dimensions for label & its text passed in 
    label = pygame.Rect(a, b, c, 30) #making a Rect for label
    pygame.draw.rect(screen, pygame.Color(24, 18, 26), label) #drawing label   
    text = "{}".format(str(level_name)) #setting text as level name
    text_surface = base_font.render(text, True,(240, 232, 213)) #rendering level name text as its surface
    text_surface_rect = text_surface.get_rect(center = (screen_width/2, b+15)) #getting Rect of text_surface
    screen.blit(text_surface, text_surface_rect) #displaying text_surface onto its Rect
             
                
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

#function to detect collisions for the tilemaps
# def tiles_collision_detection():
#     if player_rect.collidelist(tile_rects) != -1:
#         return True  # Collision detected
#     return False
     
#function used to check for doors and switch levels        
def check_for_doors(doors_group): #different level door groups passed in
    for door in doors_group: #looping through each door in the door groups to check if the player_rect is colliding with the door rect
        #print (door)
        if player_rect.colliderect(door):
            print('collision')
            level_manager.state = door.destination
            other_door = door_pairs_dict.get(door)
            offset = 50
            if other_door.door_type == "top_horizontal":
                player_rect.x = other_door.x
                player_rect.y = other_door.y + offset #switching level to that door's destination if collision occurs
            elif other_door.door_type == "bottom_horizontal":
                player_rect.x = other_door.x
                player_rect.y = other_door.y - offset
            elif other_door.door_type == "right_vertical":
                player_rect.x = other_door.x - offset
                player_rect.y = other_door.y 
            else:
                player_rect.x = other_door.x + offset
                player_rect.y = other_door.y 
            #doors_group = doors_group #storing it
    #return doors_group 
    
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
        self.moving = moving #attribute to keep track of if player is moving 
        self.value = value #attribute that increments an index
        self.direction = direction #attribute to keep track of what direction the player faces
        self.location = location #attribute to keep track of what level player is in
        self.position_resetted = False 
   
    #method used to move player
    def move_player(self, keys):
        vel = 5
        self.moving = False
        next_rect = player_rect.copy() #making a copy of player rect so collision detection can be done before moving
        # current_tile_x = player_rect.x // TILE_SIZE
        # current_tile_y = player_rect.y // TILE_SIZE
        # print(current_tile_x, current_tile_y)
      

        if keys[pygame.K_w]:#moving upwards when w key pressed by decreasing y coord of player rect by vel # and current_tile_y > 0 and maze1[current_tile_y - 1][current_tile_x] == 0:
            next_rect.y -= vel#player_rect.y -= vel
            self.direction = 'up'
            self.moving = True
        elif keys[pygame.K_s]:#moving downwards when s key pressed by increasing y coord of player rect by vel # and current_tile_y < len(maze1) - 1 and maze1[current_tile_y + 1][current_tile_x] == 0:
            next_rect.y += vel#player_rect.y += vel
            self.direction = 'down'
            self.moving = True
        elif keys[pygame.K_a]:#moving leftwards when a key pressed by decreasing x coord of player rect by vel # and current_tile_x > 0 and maze1[current_tile_y][current_tile_x - 1] == 0:
            next_rect.x -= vel#player_rect.x -= vel
            self.direction = 'left'
            self.moving = True
        elif keys[pygame.K_d]:#moving rightwards when d key pressed by increasing y coord of player rect by vel # and current_tile_x < len(maze1[0]) - 1 and maze1[current_tile_y][current_tile_x + 1] == 0:
            next_rect.x += vel#player_rect.x += vel
            self.direction = 'right'
            self.moving = True
        
        if next_rect.collidelist(tile_rects) == -1: #and not object_collision_detection():
            player_rect.update(next_rect) #letting player move only if not colliding with any occupied tiles as index of -1 within the list = not found
        # if next_rect.collidelist(bg_objects) == -1:
        #     player_rect.update(next_rect)
        else:
            self.moving = False #stopping animation if player rect is colliding with occupied tiles
    
    #method used to animate player        
    def animate_player(self):
        if self.moving:
            self.value += 0.2 #incrementing surface_lists index if player is moving
            if self.value >= len(player_surfaces_down): #resetting index back to 0 once over length of list
                self.value = 0

    #method used to draw player
    def draw_player(self):
        if self.direction == 'down':
            if self.moving == False:
                screen.blit(player_surfaces_down[0], player_rect) #down facing idle frame
            else:
                screen.blit(player_surfaces_down[int(self.value)], player_rect) #cycling through 'down' surfaces list if moving down
        elif self.direction == 'up':
            if self.moving == False:
                screen.blit(player_surfaces_up[0], player_rect) #up facing idle frame
            else:
                screen.blit(player_surfaces_up[int(self.value)], player_rect) #cycling through 'up' surfaces list if moving up
        elif self.direction == 'left':
            if self.moving == False:
                screen.blit(player_surfaces_left[0], player_rect) #left facing idle frame
            else:
                screen.blit(player_surfaces_left[int(self.value)], player_rect) #cycling through 'left' surfaces list if moving left
        elif self.direction == 'right':
            if self.moving == False:
                screen.blit(player_surfaces_right[0], player_rect) #right facing idle frame
            else:             
                screen.blit(player_surfaces_right[int(self.value)], player_rect) #cycling through 'right' surfaces list if moving right
        #pygame.draw.rect(screen, pygame.Color(0, 0, 0, a=0.1), player_rect) 

    # def reset_position(self, top_value, left_value):
    #     if self.position_resetted == False:
    #         player_rect.top = top_value
    #         player_rect.left = left_value
    #         self.position_resetted = True

    # def allow_movement(self):
    #     Allow the player to move again by setting position_resetted to False
    #     self.position_resetted = False
            
player = Player() #instantiating player object to use its methods   
player_rect = player_surfaces_down[0].get_rect() #making player_rect

class Room:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (self.width, self.height))

    #method used to draw/blit room images    
    def draw_room(self):
        #global draw_room
        screen.blit(self.image, (self.x, self.y))
        #self.width = width
        #self.height = height
        #for room in room_list:
            #room_surface = pygame.transform.scale(room, (width, height))
            #room_rect = room_surface.get_rect()
            #screen.blit(room_surface, room_rect)  
    
    def reset_position():
        pass
                 

Room_List = []        

#instantiaing room objects and appending to a room list
PeriodicalsRoom = Room_List.append(Room((screen_width-500)/2, (screen_height-700)/2, 500, 700, periodicals_room))
CopyRoom = Room_List.append(Room((screen_width-300)/2, (screen_height-500)/2, 300, 500, copy_room,))
ToiletsRoom = Room_List.append(Room((screen_width-300)/2, (screen_width-300)/2, 300, 300, toilets_room))
ChildrensRoom = Room_List.append(Room((screen_width-700)/2, (screen_height-700)/2, 700, 700, childrens_room))
StudyRoom = Room_List.append(Room((screen_width-600)/2, (screen_height-500)/2, 600, 500, study_room))
NonfictonRoom = Room_List.append(Room((screen_width-500)/2, (screen_height-700)/2, 500, 700, nonfiction_room))
MeetingRoom = Room_List.append(Room((screen_width-500)/2, (screen_height-500)/2, 500, 500, meeting_room))


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, popup):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.popup = popup #prompt to display and label item for collection
        
       
class Door(pygame.sprite.Sprite):
    def __init__(self, destination, image, door_type, x, y, width, height):
        super().__init__()
        pygame.sprite.Sprite.__init__(self) #initialising Sprite methods
        self.destination = destination #attribute to set what level each door leads to
        self.door_type = door_type
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    # def draw_door(self):
    #     screen.blit(self.image, (self.x, self.y))

 
#doors_group = pygame.sprite.Group()
#making a sprite group for doors in each level        
doors_group_periodicals = pygame.sprite.Group()
doors_group_copy = pygame.sprite.Group()
doors_group_toilets = pygame.sprite.Group()
doors_group_childrens = pygame.sprite.Group()
doors_group_study = pygame.sprite.Group()
doors_group_nonfiction = pygame.sprite.Group()
doors_group_meeting = pygame.sprite.Group()

#instantiating all doors 
door0 = Door('copy_level', horizontal_door, "top_horizontal", 250, 50, 50, 10)
door1 = Door('childrens_level', vertical_door, "right_vertical", 640, 600, 10, 50)
door2 = Door('periodicals_level', horizontal_door, "bottom_horizontal", 350, 640, 50, 10)
door3 = Door('toilets_level', vertical_door, "right_vertical", 540, 500, 10, 50)
door4 = Door('copy_level', vertical_door, "left_vertical", 250, 450, 10, 50)
door5 = Door('periodicals_level', vertical_door, "left_vertical", 50, 600, 10, 50) 
door6 = Door('study_level', horizontal_door, "top_horizontal", 350, 50, 100, 10)
door7 = Door('nonfiction_level', vertical_door, "right_vertical", 740, 300, 10, 50)
door8 = Door('childrens_level', horizontal_door, "bottom_horizontal", 400, 640, 100, 10)
door9 = Door('childrens_level', vertical_door, "left_vertical", 150, 300, 10, 50)
door10 = Door('meeting_level', horizontal_door, "top_horizontal", 350, 50, 50, 10)
door11 = Door('nonfiction_level', horizontal_door, "bottom_horizontal", 400, 640, 50, 10)
#door12 = Door('end_menu', vertical_door, 640, 350, 100, 10)

#adding doors to their corresponding door groups
doors_group_periodicals.add(door0)
doors_group_periodicals.add(door1)        
doors_group_copy.add(door2)
doors_group_copy.add(door3)
doors_group_toilets.add(door4)
doors_group_childrens.add(door5)
doors_group_childrens.add(door6)
doors_group_childrens.add(door7)
doors_group_study.add(door8)
doors_group_nonfiction.add(door9)
doors_group_nonfiction.add(door10)
doors_group_meeting.add(door11)
#doors_group_nonfiction.add(door12)

#dictionary used to associate doors together for easy repositioning of player rect when switching levels
door_pairs_dict = {
    door0: door2,
    door1: door5,
    door2: door0,
    door3: door4,
    door4: door3,
    door5: door1,
    door6: door8,
    door7: door9,
    door8: door6,
    door9: door7,
    door10: door11,
    door11: door10
    }

position_resetted = False

def reset_position(position_resetted, top_value, left_value):
    if not position_resetted:
        player_rect.top = top_value
        player_rect.left = left_value
        position_resetted = True
    return position_resetted

#function used to group invoking of functions for drawing things within each level
def levels_manage_visuals(index, maze, level_name):
    screen.fill((47, 30, 50))
    Room_List[index].draw_room()
    draw_maze(maze)
    level_labels(level_name, Room_List[index].x, Room_List[index].y+Room_List[index].height+10, Room_List[index].width)

#function used to group invoking of methods for managing the player within each level
def levels_manage_player(location):
    player.location = location
    player.draw_player()
    player.move_player(keys)
    player.animate_player()

#class to manage game states/levels 
class LevelManager:
    def __init__(self):
        self.state = 'start_menu' #setting start menu to be the first state
        #self.position_resetted = False

    # def reset_position(self, top_value, left_value):
    #     if not self.position_resetted:
    #         player_rect.top = top_value
    #         player_rect.left = left_value
    #         print("Position reset to:", top_value, left_value)
    #         self.position_resetted = True
    #     return self.position_resetted    

    #method to run the start menu    
    def start_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit program if cross clicked
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN: #proceeding with game if enter key pressed
                    self.state = 'instructions_menu' 
                elif event.key == pygame.K_ESCAPE: #quit program if esc key pressed too
                    pygame.quit()
                    sys.exit()

        screen.blit(start_menu_surface, (0, 0)) #displaying the UI image
    
    #method to run the instructions menu
    def instructions_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: #entering first level if enter key pressed
                    self.state = 'periodicals_level'
                elif event.key == pygame.K_ESCAPE: #quit program if esc key pressed too
                    pygame.quit()
                    sys.exit()    

        screen.blit(instructions, (0, 0)) #displaying the UI image 
    
    #method to run the first periodicals section level
    def periodicals_level(self):
        global position_resetted
        menu_switching('copy_level')    
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state = 'copy_level'
        
        levels_manage_visuals(0, maze1, "Periodicals Section")

        doors_group_periodicals.draw(screen) #invoking the inherited sprite method to draw all doors in periodicals door group   

        computer1 = pygame.Rect(200, 130, 50, 60)  # Create the Rect object
        bg_objects.append(computer1)  # Append it to the list
        
        computer2 = pygame.Rect(300, 130, 50, 60)
        bg_objects.append(computer2)  # Append it to the list

        table1 = pygame.Rect(230, 350, 125, 125)
        bg_objects.append(table1)  # Append it to the list

        levels_manage_player("periodicals_level")

        #self.position_resetted = self.reset_position(150, 150)
        #player.allow_movement()
        #print(player.position_resetted)
      

        #position_resetted = False
        position_resetted = reset_position(position_resetted, 150, 150)

        check_for_doors(doors_group_periodicals) #invoking method to check for collisions with perodicals doors specifically
        
        pygame.draw.rect(screen, pygame.Color('brown'), p_to_co_door) 

        # if player_rect.colliderect(p_to_co_door):
        #     player_rect.x = co_to_p_door.x
        #     player_rect.y = co_to_p_door.y - 50
        #     self.state = 'copy_level'
 
    #method to run the second copy room level    
    def copy_level(self):
        #self.position_resetted = False
        #position_resetted = reset_position(position_resetted, 150, 150)
        global position_resetted
        menu_switching('toilets_level')
        for event in pygame.event.get():
            #if event.type == keys[pygame.k_kp_enter]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                #self.state = 'toilets_level'   
                print(pygame.mouse.get_pos())     
        
        #player.position_resetted = False
        levels_manage_visuals(1, empty_maze, "Copy Room")

        #doors_group_copy.draw(screen) #invoking the inherited sprite method to draw all doors in copy door group   


        cabinet1 = pygame.Rect(255, 160, 165, 100)  # Create the Rect object
        bg_objects.append(cabinet1)  # Append it to the list
        
        drawers1 = pygame.Rect(425, 220, 125, 80)
        bg_objects.append(drawers1)  # Append it to the list
        
        copier = pygame.Rect(435, 325, 95, 120)
        bg_objects.append(copier)  # Append it to the list
       
        levels_manage_player("copy_level")
        
        #position_resetted = False
        #reset_position(position_resetted, 400, 400)

        #print(player.position_resetted)

        check_for_doors(doors_group_copy)  #invoking method to check for collisions with copy doors specifically
        
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
        menu_switching('childrens_level')        
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state =       

        levels_manage_visuals(2, empty_maze, "Toilets")

        doors_group_toilets.draw(screen) #invoking the inherited sprite method to draw all doors in toilets door group  
        
        toilets = pygame.Rect(260, 255, 155, 135)  # Create the Rect object
        bg_objects.append(toilets)  # Append it to the list
        
        cabinet2 = pygame.Rect(415, 255, 125, 80)
        bg_objects.append(cabinet2)  # Append it to the list
        
        sink = pygame.Rect(335, 490, 215, 60)
        bg_objects.append(sink)  # Append it to the list

        levels_manage_player("toilets_level")
        #print(doors_group)
        check_for_doors(doors_group_toilets)  #invoking method to check for collisions with toilets doors specifically
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
                
        levels_manage_visuals(3, maze2, "Childrens Section")

        doors_group_childrens.draw(screen)  #invoking the inherited sprite method to draw all doors in childrens door group  
  
        levels_manage_player("childrens_level")
        
        check_for_doors(doors_group_childrens) #invoking method to check for collisions with childrens doors specifically
    
    def study_level(self):
        menu_switching('nonfiction_level')        
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state =      
        
        levels_manage_visuals(4, empty_maze, "Study Room")
        
        doors_group_study.draw(screen) #invoking the inherited sprite method to draw all doors in study door group  

        table2 = pygame.Rect(105, 155, 590, 130)  # Create the Rect object
        bg_objects.append(table2)  # Append it to the list  
        
        table3 = pygame.Rect(105, 285, 125, 360)
        bg_objects.append(table3)  # Append it to the list
        
        table4 = pygame.Rect(570, 285, 125, 360)
        bg_objects.append(table4)  # Append it to the list

        levels_manage_player("study_level")

        check_for_doors(doors_group_study) #invoking method to check for collisions with study doors specifically
                
    def nonfiction_level(self):
        menu_switching('meeting_level')        
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state =       
                
        levels_manage_visuals(5, maze3, "Nonfiction Section")

        doors_group_nonfiction.draw(screen)  #invoking the inherited sprite method to draw all doors in nonfiction door group  

        table5 = pygame.Rect(235, 130, 125, 125)
        bg_objects.append(table5)  # Append it to the list

        levels_manage_player("nonfiction_level")

        check_for_doors(doors_group_nonfiction)  #invoking method to check for collisions with monfiction doors specifically


    def meeting_level(self):
        menu_switching('periodicals_level')
        # for event in pygame.event.get():
        #     #if event.type == keys[pygame.K_KP_ENTER]:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         self.state = 'meeting_level'   
                
        levels_manage_visuals(6, empty_maze, "Meeting Room")
        
        doors_group_meeting.draw(screen) #invoking the inherited sprite method to draw all doors in meeting door group  
        
        table6 = pygame.Rect(265, 350, 280, 125)  # Create the Rect object
        bg_objects.append(table6)  # Append it to the list  # Draw the Rect 
        
        cabinet3 = pygame.Rect(260, 160, 70, 80)
        bg_objects.append(cabinet3)  # Append it to the list
        
        drawers3 = pygame.Rect(340, 195, 205, 75)
        bg_objects.append(drawers3)  # Append it to the list

        levels_manage_player("meeting_level")

        check_for_doors(doors_group_meeting) #invoking method to check for collisions with meeting doors specifically
        
    def map_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_m:  #switching back to  player's location level when m key pressed again
                   self.state = player.location
                   
        screen.fill((81, 45, 45))        
        screen.blit(map_menu, (50, 150)) #displaying the UI map menu image
        
    def inventory_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  #switching back to  player's location level when m key pressed again
                    self.state = player.location  
        
        screen.fill((81, 45, 45))        
        screen.blit(inventory_menu, (50, 50)) #displaying the  UI inventory menu image
    
    #method used to run each level based on level manager state
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

#instantiating level manager object to use its methods                
level_manager = LevelManager()

while True:
   keys = pygame.key.get_pressed() #setting a keys variable for easy usage with player movement
   level_manager.level_manager() #running the level manager
   clock.tick(60) #setting framerate
