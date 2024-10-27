import pygame

#animation: tile000-008 -> down, tile020-028 -> right, tile040-048 -> up, tile060-068 -> left
player_surfaces_down = [
    pygame.transform.scale(pygame.image.load('sprite/tile000.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile001.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile002.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile003.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile004.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile005.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile006.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile007.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile008.png'), (30, 40)),
    ]
player_surfaces_right = [
    pygame.transform.scale(pygame.image.load('sprite/tile020.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile021.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile022.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile023.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile024.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile025.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile026.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile027.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile028.png'), (30, 40)),
    ]
player_surfaces_up = [
    pygame.transform.scale(pygame.image.load('sprite/tile040.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile041.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile042.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile043.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile044.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile045.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile046.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile047.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile048.png'), (30, 40)),
    ]
player_surfaces_left = [
    pygame.transform.scale(pygame.image.load('sprite/tile060.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile061.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile062.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile063.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile064.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile065.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile066.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile067.png'), (30, 40)),
    pygame.transform.scale(pygame.image.load('sprite/tile068.png'), (30, 40)),
    ]
#maze tilemap for first periodicals level
maze1 = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#0
    [3, 3, 3, 0, 0, 0, 0, 0, 1, 1, 2, 1, 2, 3, 3, 3],#1
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 3, 3, 3],#2
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 3, 3, 3],#3
    [3, 3, 3, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 3, 3, 3],#4
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 3, 3, 3],#5
    [3, 3, 3, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 3, 3, 3],#6
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 3, 3, 3],#7
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3, 3, 3],#8
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 3, 3, 3],#9
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 3, 3, 3],#10
    [3, 3, 3, 0, 1, 0, 0, 2, 1, 1, 0, 1, 1, 3, 3, 3],#11
    [3, 3, 3, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 3, 3, 3],#12
    [3, 3, 3, 0, 0, 1, 1, 1, 0, 2, 0, 1, 2, 3, 3, 3],#13
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 3, 3, 3],#14
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#15
]
#maze tilemap for first childrens and teens level
maze2 = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#0
    [3, 2, 1, 1, 1, 1, 1, 0, 0, 2, 1, 1, 1, 1, 2, 3],#1
    [3, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3],#2
    [3, 2, 1, 1, 1, 2, 0, 2, 0, 1, 1, 1, 0, 0, 2, 3],#3
    [3, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 1, 2, 3],#4
    [3, 2, 0, 2, 0, 1, 1, 1, 1, 0, 2, 0, 2, 0, 1, 3],#5
    [3, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 3],#6
    [3, 1, 1, 1, 0, 2, 1, 2, 1, 1, 2, 0, 0, 0, 2, 3],#7
    [3, 0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 1, 1, 0, 2, 3],#8
    [3, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],#9
    [3, 1, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 2, 0, 2, 3],#10
    [3, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 1, 3],#11
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 1, 1, 0, 0, 3],#12
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3],#13
    [3, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 2, 2, 2, 2, 3],#14
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#15
]
#maze tilemap for third non-fiction level
maze3 = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#0
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 3],#1
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 3, 3, 3],#2
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 3, 3, 3],#3
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3],#4
    [3, 3, 3, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 3, 3, 3],#5
    [3, 3, 3, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 3, 3, 3],#6
    [3, 3, 3, 2, 1, 2, 0, 0, 0, 0, 2, 0, 0, 3, 3, 3],#7
    [3, 3, 3, 1, 0, 1, 2, 1, 1, 1, 1, 2, 0, 3, 3, 3],#8
    [3, 3, 3, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 3, 3, 3],#9
    [3, 3, 3, 0, 2, 1, 1, 0, 2, 1, 0, 2, 0, 3, 3, 3],#10
    [3, 3, 3, 0, 1, 0, 0, 0, 2, 0, 0, 2, 0, 3, 3, 3],#11
    [3, 3, 3, 0, 0, 0, 2, 0, 1, 1, 1, 1, 0, 3, 3, 3],#12
    [3, 3, 3, 2, 0, 1, 2, 0, 0, 0, 0, 0, 0, 3, 3, 3],#13
    [3, 3, 3, 2, 0, 0, 2, 0, 0, 2, 2, 2, 0, 3, 3, 3],#14
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#15
]
