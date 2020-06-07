import pickle
import tkinter
from tkinter import *
from tkinter import simpledialog

import pygame

import Scene


def Additional_Settings(scene):

    root = Tk()
    root.title("Доп настройки.")

    forbidden_funct = Label(text="Запрещенная функция:")
    total_steps = Label(text="Максимальное количество шагов:")
    limited_funct = Label(text="Лимитированные функции:")
    forbidden_funct.grid(row=0, column=0, sticky="w")
    total_steps.grid(row=1, column=0, sticky="w")
    limited_funct.grid(row=2, column=0, sticky="w")

    forbid_entry = Entry()
    steps_entry = Entry()
    limited_entry_name = Entry()
    limited_entry_amount = Entry()
    forbid_entry.grid(row=0, column=1, padx=5, pady=5)
    forbid_button = Button(text="Запретить", command=scene.add_forbiden_func(forbid_entry.get()))
    max_steps_button = Button(text="Установить", command=scene.set_player_step_limit(steps_entry.get()))
    max_steps_button.grid(row=1, column=2, padx=5, pady=5)

    forbid_button.grid(row = 0, column = 2,padx=5, pady=5)
    steps_entry.grid(row=1, column=1, padx=5, pady=5)
    limited_entry_name.grid(row=2, column=1, padx=5, pady=5)
    limited_entry_amount.grid(row=2, column=2, padx=5, pady=5)

    limit_funct_button =Button(text="Добавить", command=scene.add_limited_function(limited_entry_name.get(),limited_entry_amount.get()))
    limit_funct_button.grid(row=2, column=3, padx=5, pady=5)
    root.mainloop()
    return scene
    # вставка начальных данных
    # name_entry.insert(0, "Tom")
    # surname_entry.insert(0, "Soyer")
    #
    # display_button = Button(text="Display", command=display)
    # clear_button = Button(text="Clear", command=clear)
    #
    # display_button.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    # clear_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")


def input_text(text="Текст задания"):
    tkinter.Tk().withdraw()
    result = simpledialog.askstring(title=text,prompt="Введите текст:")
    return result
def display_grid(scene,additional_paint = []):

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
    window_size = (size[0]*(WIDTH+MARGIN)+10,size[1]*(HEIGHT+MARGIN)+10)
    screen = pygame.display.set_mode(window_size)
    load_treat = pygame.image.load("treat.png").convert()
    load_treat = pygame.transform.scale(load_treat,(30,30))
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
                if event.key==pygame.K_5:
                  change_type="treat"
                if event.key==pygame.K_s:
                    name = input_text("Введите имя файла:")
                    if name!=None:
                        with open(name, 'wb') as output:
                            pickle.dump(scene, output, pickle.HIGHEST_PROTOCOL)
                if event.key==pygame.K_6:
                    input_text()
                if event.key==pygame.K_a:

                    scene = Additional_Settings(scene)
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
                    scene.remove_treat(column,row)
                    if scene.get_finish==(column,row):
                        scene.set_finish(-1,-1)
                    if scene.get_start==(column,row):
                        scene.set_start(-1,-1)
                if change_type=="treat":
                    scene.add_treat(column,row)
        for i in range(size[1]):
            for j in range(size[0]):
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
                if (j,i) in scene.get_treats:
                    screen.blit(load_treat,((MARGIN + WIDTH) * j + MARGIN,(MARGIN + HEIGHT) * i + MARGIN))
                if (j, i) in additional_paint:
                    pygame.draw.circle(screen,
                                       (255,0,0),
                                 [(MARGIN + WIDTH) * j + MARGIN,
                                  (MARGIN + HEIGHT) * i + MARGIN,
                                  ],int(HEIGHT/2),2)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
if __name__ == '__main__':

    scene = Scene.Scene((10, 10))
    display_grid(scene)