import pygame, sys
from pygame.locals import *
from drawer import *
from stars import *

def get_stars():
    stars = []
    path = './data/'
    txt_files = [x for x in os.listdir(path) if x.endswith('.txt')]
    for name in txt_files:
        with open(path + name) as f:
            lines = f.readlines()
            for l in lines:
                s = Star(l)
                s.x, s.y = Geom.get_image_coords(s, 1000)
                s.color = Drawer.get_color_for_pygame(s)
                stars.append(s)
    return stars


pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((1000, 1000), 0, 32)
pygame.display.set_caption('Stars')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'

stars = get_stars()


while True: # the main game loop
    DISPLAYSURF.fill(BLACK)

    pos = pygame.mouse.get_pos()
    # print(pos)
    # pygame.draw.line(DISPLAYSURF, (  0, 255,   0), [0, 0], pos, 5)
    # pygame.draw.circle(DISPLAYSURF, (  255,  0, 0), pos, 6)

    for s in stars:
        pygame.draw.circle(DISPLAYSURF, s.color, [int(s.x), int(s.y)], 2)
        if abs(int(s.x) - pos[0]) < 9 and abs(int(s.y) - pos[1]) < 9:
            print(pos)
            pygame.draw.circle(DISPLAYSURF, (  255,   0, 0), [int(s.x), int(s.y)], 2)

        # pygame.draw.line(DISPLAYSURF, (  0,   0, 255), [int(s.x), int(s.y)], [int(s.x), int(s.y)], 1)
        # if direction == 'right':
        #     s.x+=1
        # elif direction == 'down':
        #     s.y+=1
        # elif direction == 'left':
        #     s.x-=1
        # elif direction == 'up':
        #     s.y-=1

    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    DISPLAYSURF.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)