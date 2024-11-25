# File: 13DT_programming_game.py
# Author: Sophy Liang
# Date created: 23/07/2024
# Description: This script is a computer map-based adventure game, set in a library, where the player collects items.  
# User inputs: Keyboard controls only

import pygame, sys
from maze_tilemaps_and_sprite_frames import player_surfaces_down, player_surfaces_left, player_surfaces_right, player_surfaces_up, maze1, maze2, maze3, copy_room_tilemap, toilet_tilemap, study_tilemap, meeting_tilemap

# CLASSES

# class to make the player character
class Player:
    def __init__(self, moving=False, value=0, direction='right', location='periodicals_level', position_resetted=False):
        self.moving = moving # keeps track of if player is moving 
        self.value = value # increments an index
        self.direction = direction # keeps track of what direction the player faces
        self.location = location # keeps track of what level player is in
        self.position_resetted = position_resetted # keeps track of if player's position has been reset
   
    # method used to move player
    def move_player(self, keys):
        VEL = 7
        self.moving = False
        next_rect = player_rect.copy() # making a copy of player rect so collision detection can be done before moving

        if keys[pygame.K_w]:# moving upwards when w key pressed by decreasing y coord of player rect by vel 
            next_rect.y -= VEL 
            self.direction = 'up'
            self.moving = True
        elif keys[pygame.K_s]:# moving downwards when s key pressed by increasing y coord of player rect by vel # 
            next_rect.y += VEL 
            self.direction = 'down'
            self.moving = True
        elif keys[pygame.K_a]:# moving leftwards when a key pressed by decreasing x coord of player rect by vel # 
            next_rect.x -= VEL 
            self.direction = 'left'
            self.moving = True
        elif keys[pygame.K_d]:# moving rightwards when d key pressed by increasing y coord of player rect by vel 
            next_rect.x += VEL 
            self.direction = 'right'
            self.moving = True
        
        if next_rect.collidelist(tile_rects) == -1: 
            player_rect.update(next_rect) # letting player move only if not colliding with any occupied tiles as index of -1 within the list = not found
        else:
            self.moving = False # stopping animation if player rect is colliding with occupied tiles
    
    # method used to animate player        
    def animate_player(self):
        if self.moving:
            self.value += 0.2 # incrementing surface_lists index if player is moving
            if self.value >= len(player_surfaces_down): # resetting index back to 0 once over length of list
                self.value = 0

    # method used to draw player
    def draw_player(self):
        if self.direction == 'down':
            if self.moving == False:
                screen.blit(player_surfaces_down[0], player_rect) # down facing idle frame
            else:
                screen.blit(player_surfaces_down[int(self.value)], player_rect) # cycling through 'down' surfaces list if moving down
        elif self.direction == 'up':
            if self.moving == False:
                screen.blit(player_surfaces_up[0], player_rect) # up facing idle frame
            else:
                screen.blit(player_surfaces_up[int(self.value)], player_rect) # cycling through 'up' surfaces list if moving up
        elif self.direction == 'left':
            if self.moving == False:
                screen.blit(player_surfaces_left[0], player_rect) # left facing idle frame
            else:
                screen.blit(player_surfaces_left[int(self.value)], player_rect) #c ycling through 'left' surfaces list if moving left
        elif self.direction == 'right':
            if self.moving == False:
                screen.blit(player_surfaces_right[0], player_rect) # right facing idle frame
            else:             
                screen.blit(player_surfaces_right[int(self.value)], player_rect) #c ycling through 'right' surfaces list if moving right
    
    # method used to reset player's position after game is over or won
    def reset_position(self, top_value, left_value):
        if not self.position_resetted:
            self.direction = 'right'
            player_rect.top = top_value
            player_rect.left = left_value
            self.position_resetted = True

# class to make the rooms 
class Room:
    def __init__(self, x, y, width, height, image, tilemap):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.tilemap = tilemap

    # method used to draw/blit room images    
    def draw_room(self):
        screen.blit(self.image, (self.x, self.y))   
        
# class to make item sprite objects
class Item(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, width=0, height=0, image=None, inventory_image=None, 
                 inventory_x=0, inventory_y=0, map_image=None, right_notif_popup_active=False): 
        # keeping all params default so I can instantiate a default object to use this classes methods
        super().__init__()
        pygame.sprite.Sprite.__init__(self) # initialising Sprite methods
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image 
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) 
        self.inventory_image = inventory_image # the true image for hidden items
        self.inventory_x = inventory_x # x-coord for display/drawing in inventory slot
        self.inventory_y = inventory_y # y-coord for display/drawing in inventory slot
        self.map_image = map_image # the new map to be displayed after item is collected
        self.right_notif_popup_active = right_notif_popup_active # keeps track of if the notif is up or not
    
    # method used to handle player collecting the right item
    def right_item_collection(self, keys, item, popup, items_group, popups_group, item_collected_popup, item_collected_popup_group, 
                              door, door_group, events):
        items_group.draw(screen)  # drawing items and popups
        if player_rect.colliderect(item):
            popups_group.draw(screen)
            if keys[pygame.K_c] and not self.right_notif_popup_active:
                    item.kill()  # killing item and popup
                    popup.kill()
                    self.right_notif_popup_active = True  # marking popup as active
                    found_items.append(item)
                    pygame.time.set_timer(KILL_RIGHT_NOTIF_POPUP, 1500) # starting timer
                    door_group.add(door)  # addding door after popup is displayed
                    
        if self.right_notif_popup_active:
            item_collected_popup_group.draw(screen)

        for event in events:  # handling timer to kill collected popup
            if event.type == KILL_RIGHT_NOTIF_POPUP and self.right_notif_popup_active:
                item_collected_popup.kill()
                self.right_notif_popup_active = False  # reset popup state
                pygame.time.set_timer(KILL_RIGHT_NOTIF_POPUP, 0)
                item_collected_popup_group.add(Item_Collected_Popup)
     
    # method used to handle player collecting the wrong item            
    def wrong_item_collection(self, keys, item, items_group, popups_group):
        items_group.draw(screen) # draw items and popups
        if player_rect.colliderect(item):
            popups_group.draw(screen)
            if keys[pygame.K_c]:
                    level_manager.state = 'game_over' # making it game over        
                
 # class to make popup sprite objects
class Popup(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        pygame.sprite.Sprite.__init__(self) # initialising Sprite methods
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

# class to make door sprite objects
class Door(pygame.sprite.Sprite):
    def __init__(self, destination, image, door_type, x, y, width, height):
        super().__init__()
        pygame.sprite.Sprite.__init__(self) # initialising Sprite methods
        self.destination = destination # setting what level each door leads to
        self.door_type = door_type # setting on which wall the door is placed
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

# class to manage game states/levels 
class LevelManager:
    def __init__(self):
        self.state = 'start_menu' # setting start menu to be the first state

    # method used to run the start menu    
    def start_menu(self, events):
        for event in events:
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN: # proceeding with game if enter key pressed
                    self.state = 'instructions_menu' 
                elif event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()

        screen.blit(start_menu_surface, (0, 0)) # displaying the UI image
    
    # method used to run the instructions menu
    def instructions_menu(self, events):
       for event in events:
            if event.type == pygame.quit:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #entering first level if enter key pressed
                    self.state = 'periodicals_level'
                elif event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()    
                    
       screen.blit(instructions, (0, 0)) #displaying the UI image 
    
    # method to used to run the first level
    def periodicals_level(self, events):
        player.reset_position(150, 150)
        menu_switching(events)
        levels_manage_rendering(0, PeriodicalsRoom, "Periodicals Section")  
        levels_manage_player("periodicals_level")
        default_item.right_item_collection(keys, Magazine, Magazine_Popup, items_group_periodicals, popups_group_periodicals,
                                           Item_Collected_Popup, item_collected_popup_group,
                                           door0, doors_group_periodicals, events)
        default_item.wrong_item_collection(keys, Shakespearean_Collection, items_group_periodicals2, popups_group_periodicals2)
        draw_and_check_for_doors(doors_group_periodicals) 

    # method to used to run the second level
    def copy_level(self, events):
        menu_switching(events)   
        levels_manage_rendering(1, CopyRoom, "Copy Room") 
        levels_manage_player("copy_level")
        default_item.right_item_collection(keys, Sheet_Music, Sheet_Music_Popup, items_group_copy, 
                                             popups_group_copy, Item_Collected_Popup, item_collected_popup_group, 
                                             door3, doors_group_copy, events)
        draw_and_check_for_doors(doors_group_copy)
 
    # method to used to run the third level    
    def toilets_level(self, events):
        menu_switching(events)           
        levels_manage_rendering(2, ToiletsRoom, "Toilets")  
        levels_manage_player("toilets_level")
        default_item.right_item_collection(keys, Newspaper, Newspaper_Popup, items_group_toilets, 
                                             popups_group_toilets, Item_Collected_Popup, item_collected_popup_group, 
                                             door1, doors_group_periodicals, events)
        draw_and_check_for_doors(doors_group_toilets) 
        
    # method to used to run the fourth level   
    def childrens_level(self, events):
        menu_switching(events)                     
        levels_manage_rendering(3, ChildrensRoom, "Childrens Section")
        levels_manage_player("childrens_level")
        default_item.right_item_collection(keys, Comic_Book, Comic_Book_Popup, items_group_childrens, 
                                             popups_group_childrens, Item_Collected_Popup, item_collected_popup_group, 
                                             door6, doors_group_childrens, events)
        default_item.wrong_item_collection(keys, Academic_Journal, items_group_childrens2, popups_group_childrens2)
        draw_and_check_for_doors(doors_group_childrens) 
    
    # method to used to run the fifth level  
    def study_level(self, events):
        menu_switching(events)        
        levels_manage_rendering(4, StudyRoom, "Study Room") 
        levels_manage_player("study_level")
        default_item.right_item_collection(keys, Dvd, Dvd_Popup, items_group_study, 
                                             popups_group_study, Item_Collected_Popup, item_collected_popup_group, 
                                             door7, doors_group_childrens, events)
        draw_and_check_for_doors(doors_group_study) 
        
    # method to used to run the sixth level  
    def nonfiction_level(self, events):
        menu_switching(events)                    
        levels_manage_rendering(5, NonfictonRoom, "Nonfiction Section")
        levels_manage_player("nonfiction_level")
        default_item.right_item_collection(keys, Cookbook, Cookbook_Popup, items_group_nonfiction, 
                                             popups_group_nonfiction, Item_Collected_Popup, item_collected_popup_group, 
                                             door10, doors_group_nonfiction, events)
        default_item.wrong_item_collection(keys, Fairytale, items_group_nonfiction2, popups_group_nonfiction2)
        draw_and_check_for_doors(doors_group_nonfiction)
        
    # method to used to run the seventh level     
    def meeting_level(self, events):
        menu_switching(events)       
        levels_manage_rendering(6, MeetingRoom, "Meeting Room")
        levels_manage_player("meeting_level")
        default_item.right_item_collection(keys, Self_Help_Book, Self_Help_Book_Popup, items_group_meeting, 
                                             popups_group_meeting, Item_Collected_Popup, item_collected_popup_group, 
                                             door12, doors_group_nonfiction, events)
        draw_and_check_for_doors(doors_group_meeting)
     
    # method to used to run the map menu         
    def map_menu(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_n:  # switching back to player's location level when n key pressed 
                   self.state = player.location  
                   
        screen.fill((81, 45, 45))  
        screen.blit(map_menu1, (50, 150)) # displaying the UI map menu image
        draw_map(found_items)
    
    # method to used to run the inventory menu    
    def inventory_menu(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  #switching back to player's location level when r key pressed 
                    self.state = player.location  

        screen.fill((81, 45, 45))        
        screen.blit(inventory_menu, (50, 50)) #displaying the  UI inventory menu image
        draw_collected_item(found_items)   
    
    # method to used to run the game won screen    
    def game_won(self, events, found_items):
        for event in events:
            if event.type == pygame.quit:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # back to start menu if enter key pressed
                    self.state = 'start_menu'
                elif event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()    
                    
        screen.blit(game_won_screen, (0, 0))
        reset_game(found_items)
        
    # method to used to run the game over screen   
    def game_over(self, events, found_items):
        for event in events:
            if event.type == pygame.quit:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # back to start menu if enter key pressed
                    self.state = 'start_menu'
                elif event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()    
                    
        screen.blit(game_over_screen, (0, 0))
        reset_game(found_items)
 
    # method used to run each level based on level manager state
    def level_manager(self):
        if self.state == 'start_menu':
            self.start_menu(events)
        if self.state == 'instructions_menu':
            self.instructions_menu(events)
        if self.state == 'periodicals_level':
            self.periodicals_level(events)
        if self.state == 'copy_level':
            self.copy_level(events)
        if self.state == 'toilets_level':
            self.toilets_level(events)
        if self.state == 'childrens_level':
            self.childrens_level(events)
        if self.state == 'study_level':
            self.study_level(events)
        if self.state == 'nonfiction_level':
            self.nonfiction_level(events)
        if self.state == 'meeting_level':
            self.meeting_level(events)
        if self.state == 'map_menu':
            self.map_menu(events)
        if self.state == 'inventory_menu':
            self.inventory_menu(events)
        if self.state == 'game_won':
            self.game_won(events, found_items)
        if self.state == 'game_over':
            self.game_over(events, found_items)
        pygame.display.update()                  

# FUNCTIONS

# function used to draw tilemaps
def draw_tilemap(maze): # maze lists are passed in to draw them 
    tile_rects.clear() 
    for row in range(len(maze)): # iterating through each row in the maze
        for column in range(len(maze[row])): # iterating through each column in current row
            x = column * TILE_SIZE # calculating x-coord for tile
            y = row * TILE_SIZE # calculating y-coord for tile
            tile = tiles[maze[row][column]] # getting right tile based on maze value
            screen.blit(tile, (x, y)) # drawing tile at calculate coords
            
            # getting rects of occupied tiles & adding them to tile rects list for collision detection
            if maze[row][column] in solid_tile_indices: 
                tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                tile_rects.append(tile_rect)                          
    
# function used to draw/blit labels to name each level 
def level_labels(level_name, topleft_x, topleft_y, width): # level name, & dimensions for label & its text passed in 
    label = pygame.Rect(topleft_x, topleft_y, width, 30) # making a Rect for label
    pygame.draw.rect(screen, pygame.Color(24, 18, 26), label) # drawing label   
    text = "{}".format(str(level_name)) # setting text as level name
    text_surface = base_font.render(text, True,(240, 232, 213)) # rendering level name text as its surface
    text_surface_rect = text_surface.get_rect(center = (SCREEN_WIDTH/2, topleft_y+15)) # getting Rect of text_surface
    screen.blit(text_surface, text_surface_rect) # displaying text_surface onto its Rect

# function used to check for doors and switch levels        
def draw_and_check_for_doors(doors_group): # different level door groups passed in
    doors_group.draw(screen)
    for door in doors_group: 
        # looping through each door in the door groups to check if player_rect is colliding with door rect
        if player_rect.colliderect(door):
            level_manager.state = door.destination 
            # switching level to that door's destination if collision occurs
            other_door = door_pairs_dict.get(door) 
            # getting other door in the pair in the dictionary to use its coords
            offset = 50
            if other_door.door_type == "top_horizontal": 
                player_rect.x = other_door.x
                player_rect.y = other_door.y + offset 
            elif other_door.door_type == "bottom_horizontal":
                player_rect.x = other_door.x
                player_rect.y = other_door.y - offset
            elif other_door.door_type == "right_vertical":
                player_rect.x = other_door.x - offset
                player_rect.y = other_door.y 
            else:
                player_rect.x = other_door.x + offset
                player_rect.y = other_door.y       
                # adjusting player sprite position based on door type so they end up inside new level's confines
                
# function used to handle exiting & switching into map & inventory menu within each room/level
def menu_switching(events): 
    for event in events: # using pygame events to handle user input 
        if event.type == pygame.QUIT: # quit program if cross is clicked
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: # switching into map if m key is pressed
            if event.key == pygame.K_m:
                level_manager.state = 'map_menu'
            elif event.key == pygame.K_e: # switching into inventory is e key is pressed
                level_manager.state = 'inventory_menu'  
                
# function used to add items and popups to their exclusive group
def add_items_and_popups_to_groups():
    items_group_periodicals.add(Magazine)
    popups_group_periodicals.add(Magazine_Popup)
    items_group_periodicals2.add(Shakespearean_Collection)
    popups_group_periodicals2.add(Shakespearean_Collection_Popup)

    items_group_copy.add(Sheet_Music)
    popups_group_copy.add(Sheet_Music_Popup)

    items_group_toilets.add(Newspaper)
    popups_group_toilets.add(Newspaper_Popup)

    items_group_childrens.add(Comic_Book)
    popups_group_childrens.add(Comic_Book_Popup)
    items_group_childrens2.add(Academic_Journal)
    popups_group_childrens2.add(Academic_Journal_Popup)

    items_group_study.add(Dvd)
    popups_group_study.add(Dvd_Popup)

    items_group_nonfiction.add(Cookbook)
    popups_group_nonfiction.add(Cookbook_Popup)
    items_group_nonfiction2.add(Fairytale)
    popups_group_nonfiction2.add(Fairytale_Popup)

    items_group_meeting.add(Self_Help_Book)
    popups_group_meeting.add(Self_Help_Book_Popup)

    item_collected_popup_group.add(Item_Collected_Popup)
    wrong_item_popup_group.add(Wrong_Item_Popup)
      
# function used to group invoking of functions for drawing things within each level
def levels_manage_rendering(index, room, level_name):
    screen.fill((47, 30, 50))
    Room_List[index].draw_room()
    draw_tilemap(room.tilemap)
    level_labels(level_name, Room_List[index].x, Room_List[index].y+Room_List[index].height+10, Room_List[index].width)

# function used to group invoking of methods for managing the player within each level
def levels_manage_player(location):
    player.location = location
    player.draw_player()
    player.move_player(keys)
    player.animate_player()

# function used to reset the game
def reset_game(found_items):
        player.position_resetted = False # resetting player position to start
        for item in found_items:
            item.image = pygame.transform.scale(item.image, (50, 50)) # reducing size of image back to 50x50
        add_items_and_popups_to_groups() # adding items and popups back into their groups so they can be shown
        door0.kill() # killing the doors that give new level access 
        door1.kill()
        door3.kill()
        door6.kill()
        door7.kill()
        door10.kill()
        door12.kill()
        
# function used to display/draw collected items in inventory
def draw_collected_item(found_items):
    for item in found_items:
        if item.inventory_image != None:
            item.inventory_image = pygame.transform.scale(item.inventory_image, (100, 100)) # enlarging size of image to 100x100 for slots in inventory
            screen.blit(item.inventory_image, (item.inventory_x, item.inventory_y))
        else:
            item.image = pygame.transform.scale(item.image, (100, 100)) # enlarging size of image to 100x100 for slots in inventory
            screen.blit(item.image, (item.inventory_x, item.inventory_y))
            
# function used to draw the new map after each new collected item
def draw_map(found_items):
    for item in found_items:
        screen.blit(item.map_image, (50, 150))
        
# SETUP, CONSTANTS & ASSETS/IMAGES

# intialising pygame and setting font
pygame.init()
pygame.font.init()
pygame.mixer.pre_init(frequency= 44100, size = 16, channels=1, buffer=512)
base_font = pygame.font.Font('assets/PixelifySans-Regular.ttf',32)
right_ding = pygame.mixer.Sound('assets/ding-36029.mp3') # not used 
pygame.mouse.set_visible(False)

# setting up the screen and its dimensions, clock
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# event used to update the screen
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# event used to kill the notif after a time delay
KILL_RIGHT_NOTIF_POPUP = pygame.USEREVENT + 1

# room and door images
periodicals_room = pygame.image.load('assets/periodicals_final1.png')
copy_room = pygame.image.load('assets/copy_room_final2.png')
toilets_room = pygame.image.load('assets/toilets_final.png')
childrens_room = pygame.image.load('assets/childrens_final2.png')
study_room = pygame.image.load('assets/studyroom_final.png')
nonfiction_room = pygame.image.load('assets/nonfiction_final.png')
meeting_room = pygame.image.load('assets/meeting_room_definite_final.png')
vertical_door = pygame.transform.scale(pygame.image.load('assets/vertical_door.png'), (10, 50))
horizontal_door = pygame.transform.scale(pygame.image.load('assets/horizontal_door.png'), (50, 10))

# menu images
map_menu1 = pygame.transform.scale(pygame.image.load('assets/game_map1.png'), (700, 500))
map_menu2 = pygame.transform.scale(pygame.image.load('assets/game_map2.png'), (700, 500))
map_menu3 = pygame.transform.scale(pygame.image.load('assets/game_map3.png'), (700, 500))
map_menu4 = pygame.transform.scale(pygame.image.load('assets/game_map4.png'), (700, 500))
map_menu5 = pygame.transform.scale(pygame.image.load('assets/game_map5.png'), (700, 500))
map_menu6 = pygame.transform.scale(pygame.image.load('assets/game_map6.png'), (700, 500))
map_menu7 = pygame.transform.scale(pygame.image.load('assets/proper_game_map_whole.png'), (700, 500))
inventory_menu = pygame.transform.scale(pygame.image.load('assets/totebag.png'), (700, 700))
start_menu_surface = pygame.transform.scale(pygame.image.load('assets/start_menu_1.png'), (800, 800))
instructions = pygame.transform.scale(pygame.image.load('assets/instructions_final_final.png'), (800, 800))
game_won_screen = pygame.transform.scale(pygame.image.load('assets/game_won.png'), (800, 800))
game_over_screen = pygame.transform.scale(pygame.image.load('assets/game_over_screen_final.png'), (800, 800))

# item images
magazine = pygame.transform.scale(pygame.image.load('assets/magazine.png'), (50, 50))
sheet_music = pygame.transform.scale(pygame.image.load('assets/sheet_music.png'), (50, 50))
newspaper = pygame.transform.scale(pygame.image.load('assets/newspaper.png'), (50, 50))
comic_book = pygame.transform.scale(pygame.image.load('assets/comic_book.png'), (50, 50))
dvd = pygame.transform.scale(pygame.image.load('assets/dvd.png'), (50, 50))
cookbook = pygame.transform.scale(pygame.image.load('assets/cookbook.png'), (50, 50))
self_help = pygame.transform.scale(pygame.image.load('assets/self_help_book.png'), (50, 50))
shakespearean_collection = pygame.transform.scale(pygame.image.load('assets/shakespearean_collection.png'), (50, 50))
academic_journal = pygame.transform.scale(pygame.image.load('assets/academic_journal.png'), (50, 50))
fairytale = pygame.transform.scale(pygame.image.load('assets/fairytale.png'), (50, 50))

# collect popup images
magazine_popup = pygame.transform.scale(pygame.image.load('assets/magazine_popup.png'), (175, 40))
sheet_music_popup = pygame.transform.scale(pygame.image.load('assets/sheet_music_popup.png'), (175, 40))
newspaper_popup = pygame.transform.scale(pygame.image.load('assets/newspaper_popup.png'), (175, 40))
comic_book_popup = pygame.transform.scale(pygame.image.load('assets/comic_book_popup.png'), (175, 40))
dvd_popup = pygame.transform.scale(pygame.image.load('assets/dvd_popup.png'), (175, 40))
cookbook_popup = pygame.transform.scale(pygame.image.load('assets/cookbook_popup.png'), (175, 40))
self_help_popup = pygame.transform.scale(pygame.image.load('assets/self_help_book_popup.png'), (175, 40))
shakespearean_collection_popup = pygame.transform.scale(pygame.image.load('assets/shakespearean_collection_popup.png'), (175, 40))
academic_journal_popup = pygame.transform.scale(pygame.image.load('assets/academic_journal_popup.png'), (175, 40))
fairytale_popup = pygame.transform.scale(pygame.image.load('assets/fairytale_popup.png'), (175, 40))
item_collected_popup = pygame.transform.scale(pygame.image.load('assets/item_collected_popup.png'), (175, 40))
wrong_item_popup = pygame.transform.scale(pygame.image.load('assets/wrong_item_popup.png'), (175, 40))

# tile images 
empty = pygame.transform.scale(pygame.image.load("assets/empty.png"), (50, 50))  
bookshelf = pygame.transform.scale(pygame.image.load("assets/bookshelve.png"), (50, 50))    
bookshelftop = pygame.transform.scale(pygame.image.load("assets/bookshelftop.png"), (50, 50))   
wall = pygame.transform.scale(pygame.image.load("assets/wall.png"), (50, 50)) 

TILE_SIZE = 50 # size of square tiles for tilemaps
tiles = [empty, bookshelf, bookshelftop, wall] # a list of tiles surfaces used
tile_rects = [] # a list of tile rects used for collision detection
solid_tile_indices = [1, 2, 3] # indices of occupied tiles
            
# INSTANTIATING OBJECTS

player = Player() # instantiating player object to use its methods   
player_rect = player_surfaces_right[0].get_rect() # making player_rect

#instantiaing room objects and appending to a room list
Room_List = [] 
PeriodicalsRoom = Room((SCREEN_WIDTH-500)/2, (SCREEN_HEIGHT-700)/2, 500, 700, periodicals_room, maze1)
Room_List.append(PeriodicalsRoom)
CopyRoom = Room((SCREEN_WIDTH-300)/2, (SCREEN_HEIGHT-500)/2, 300, 500, copy_room, copy_room_tilemap)
Room_List.append(CopyRoom)
ToiletsRoom = Room((SCREEN_WIDTH-300)/2, (SCREEN_HEIGHT-300)/2, 300, 300, toilets_room, toilet_tilemap)
Room_List.append(ToiletsRoom)
ChildrensRoom = Room((SCREEN_WIDTH-700)/2, (SCREEN_HEIGHT-700)/2, 700, 700, childrens_room, maze2)
Room_List.append(ChildrensRoom)
StudyRoom = Room((SCREEN_WIDTH-600)/2, (SCREEN_HEIGHT-500)/2, 600, 500, study_room, study_tilemap)
Room_List.append(StudyRoom)
NonfictonRoom = Room((SCREEN_WIDTH-500)/2, (SCREEN_HEIGHT-700)/2, 500, 700, nonfiction_room, maze3)
Room_List.append(NonfictonRoom)
MeetingRoom = Room((SCREEN_WIDTH-500)/2, (SCREEN_HEIGHT-500)/2, 500, 500, meeting_room, meeting_tilemap)
Room_List.append(MeetingRoom)
     
#instantiating all the items and popups
found_items = []

default_item = Item()

Magazine = Item(500, 340, 50, 50, magazine, None, 350, 295, map_menu2)
Magazine_Popup = Popup(550, 340, 175, 40, magazine_popup)
Shakespearean_Collection = Item(540, 540, 50, 50, shakespearean_collection)
Shakespearean_Collection_Popup = Popup(590, 540, 175, 40, shakespearean_collection_popup)

Sheet_Music = Item(440, 410, 50, 50, empty, sheet_music, 475, 360, map_menu3)
Sheet_Music_Popup = Popup(490, 410, 175, 40, sheet_music_popup)

Newspaper = Item(480, 340, 50, 50, empty, newspaper, 475, 505, map_menu4)
Newspaper_Popup = Popup(530, 340, 175, 40, newspaper_popup)

Comic_Book = Item(100, 340, 50, 50, comic_book, None, 350, 585, map_menu5)
Comic_Book_Popup = Popup(150, 340, 175, 40, comic_book_popup)
Academic_Journal = Item(550, 590, 50, 50, academic_journal)
Academic_Journal_Popup = Popup(600, 590, 175, 40, academic_journal_popup)

Dvd = Item(505, 240, 50, 50, empty, dvd, 225, 505, map_menu6)
Dvd_Popup = Popup(555, 240, 175, 40, dvd_popup)

Cookbook = Item(460, 490, 50, 50, cookbook, None, 225, 355, map_menu7)
Cookbook_Popup = Popup(510, 490, 175, 40, cookbook_popup)
Fairytale = Item(240, 640, 50, 50, fairytale)
Fairytale_Popup = Popup(290, 640, 175, 40, fairytale_popup)

Self_Help_Book = Item(240, 380, 50, 50, self_help, None, 350, 430, map_menu7)
Self_Help_Book_Popup = Popup(290, 380, 175, 40, self_help_popup)

Item_Collected_Popup = Popup(625, 0, 175, 40, item_collected_popup) # changed from bottom right to top right so it didn't overlap any level labels
Wrong_Item_Popup = Popup(625, 0, 175, 40, wrong_item_popup)

# sprite groups for the items
items_group_periodicals = pygame.sprite.Group()
items_group_periodicals2 = pygame.sprite.Group()
items_group_copy = pygame.sprite.Group()
items_group_toilets = pygame.sprite.Group()
items_group_childrens = pygame.sprite.Group()
items_group_childrens2 = pygame.sprite.Group()
items_group_study = pygame.sprite.Group()
items_group_nonfiction = pygame.sprite.Group()
items_group_nonfiction2 = pygame.sprite.Group()
items_group_meeting = pygame.sprite.Group()

# sprite groups for the items popups
popups_group_periodicals = pygame.sprite.Group()
popups_group_periodicals2 = pygame.sprite.Group()
popups_group_copy = pygame.sprite.Group()
popups_group_toilets = pygame.sprite.Group()
popups_group_childrens = pygame.sprite.Group()
popups_group_childrens2 = pygame.sprite.Group()
popups_group_study = pygame.sprite.Group()
popups_group_nonfiction = pygame.sprite.Group()
popups_group_nonfiction2 = pygame.sprite.Group()
popups_group_meeting = pygame.sprite.Group()

# sprite group for the notif
item_collected_popup_group = pygame.sprite.Group()
wrong_item_popup_group = pygame.sprite.Group()
    
add_items_and_popups_to_groups()
      
# sprite groups for doors in each level        
doors_group_periodicals = pygame.sprite.Group()
doors_group_copy = pygame.sprite.Group()
doors_group_toilets = pygame.sprite.Group()
doors_group_childrens = pygame.sprite.Group()
doors_group_study = pygame.sprite.Group()
doors_group_nonfiction = pygame.sprite.Group()
doors_group_meeting = pygame.sprite.Group()

# instantiating all doors 
door0 = Door('copy_level', horizontal_door, "top_horizontal", 250, 50, 50, 10)
door1 = Door('childrens_level', vertical_door, "right_vertical", 640, 600, 10, 50)
door2 = Door('periodicals_level', horizontal_door, "bottom_horizontal", 350, 640, 50, 10)
door3 = Door('toilets_level', vertical_door, "right_vertical", 540, 500, 10, 50)
door4 = Door('copy_level', vertical_door, "left_vertical", 250, 450, 10, 50)
door5 = Door('periodicals_level', vertical_door, "left_vertical", 50, 600, 10, 50) 
door6 = Door('study_level', horizontal_door, "top_horizontal", 400, 50, 100, 10)
door7 = Door('nonfiction_level', vertical_door, "right_vertical", 740, 300, 10, 50)
door8 = Door('childrens_level', horizontal_door, "bottom_horizontal", 400, 640, 100, 10)
door9 = Door('childrens_level', vertical_door, "left_vertical", 150, 300, 10, 50)
door10 = Door('meeting_level', horizontal_door, "top_horizontal", 350, 50, 50, 10)
door11 = Door('nonfiction_level', horizontal_door, "bottom_horizontal", 400, 640, 50, 10)
door12 = Door('game_won', vertical_door, "left_vertical", 640, 350, 10, 50)

# adding non-new level access doors to their corresponding door groups     
doors_group_copy.add(door2)
doors_group_toilets.add(door4)
doors_group_childrens.add(door5)
doors_group_study.add(door8)
doors_group_nonfiction.add(door9)
doors_group_meeting.add(door11)

# dictionary used to associate doors together for easy repositioning of player rect when switching levels
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
    door11: door10,
    door12: door0
    }

# instantiating level manager object to use its methods                
level_manager = LevelManager()

while True:
   keys = pygame.key.get_pressed() # setting a keys variable for easy usage with key inputs
   events = pygame.event.get()
   level_manager.level_manager() # running the level manager
   clock.tick(60) # setting framerate

