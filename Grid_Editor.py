import pygame

import Scene


def display_grid(scene):
    size = scene.get_size
    change_type = "block"
    grid = []
    for i in range(size[0]):
        grid.append([])
        for j in range(size[1]):
            grid[i].append(0)
    WIDTH = 40
    HEIGHT = 40
    MARGIN = 5
    pygame.init()
    window_size = (size[1]*(WIDTH+MARGIN)+10,size[0]*(WIDTH+MARGIN)+10)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("GridView")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    change_type = "start"
                if event.key==pygame.K_2:
                    change_type= "block"
                if event.key==pygame.K_3:
                    change_type="finish"
                if event.key==pygame.K_4:
                    change_type="clear"
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if change_type=="block":
                    scene.block_cell(column,row)
                if change_type=="finish":
                    scene.set_finish(column,row)
                if change_type=="start":
                    scene.set_start(column,row)
                if change_type=="clear":
                    scene.unblock_cell(column,row)
                    if scene.get_finish==(column,row):
                        scene.set_finish(-1,-1)
                    if scene.get_start==(column,row):
                        scene.set_start(-1,-1)
        for i in range(size[0]):
            for j in range(size[1]):
                color = (255,255,255)
                if (j,i)in scene.get_blocked:
                    color = (0,0,255)
                elif (j,i)==scene.get_start:
                    color=(0,200,0)
                elif (j,i)==scene.get_finish:
                    color=(255,215,0)
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * j + MARGIN,
                                  (MARGIN + HEIGHT) * i + MARGIN,
                                  WIDTH,
                                  HEIGHT])
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
display_grid(Scene.Scene())