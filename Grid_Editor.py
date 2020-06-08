import pickle
import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter.scrolledtext import ScrolledText

import pygame

import Scene


def Show_Scene_Info(scene):
    print("Start:" + str(scene.get_start))
    print("Finish:"+str(scene.get_finish))
    print("Max_Steps:"+str(scene.get_player_step_limit))
    print("Limited Functions:"+str(scene.get_limited_functions))
    print("Mud cells:"+str(scene.get_mud_cells))
    print("mandatory_functions:"+str(scene.get_mandatoy_functions))
    print("Start_Code:\n"+scene.get_start_code)
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
    forbid_button = Button(text="Запретить", command=lambda : scene.add_forbiden_func(forbid_entry.get()))
    max_steps_button = Button(text="Установить", command=lambda : scene.set_player_step_limit(steps_entry.get()))
    max_steps_button.grid(row=1, column=2, padx=5, pady=5)

    forbid_button.grid(row = 0, column = 2,padx=5, pady=5,sticky="e")
    steps_entry.grid(row=1, column=1, padx=5, pady=5)
    limited_entry_name.grid(row=2, column=1, padx=5, pady=5)
    limited_entry_amount.grid(row=2, column=2, padx=5, pady=5)

    limit_funct_button =Button(text="Добавить", command=lambda : scene.add_limited_function(limited_entry_name.get(),limited_entry_amount.get()))
    limit_funct_button.grid(row=2, column=3, padx=5, pady=5)
    show_info_button = Button(text="Просмотреть ограничения.",command = lambda : Show_Scene_Info(scene))
    mandatory_function_entry = Entry()
    mandatory_function_entry.grid(row=3, column=1, padx=5, pady=5)
    mandatory_label = Label(text="Обязательная функция:")
    mandatory_label.grid(row = 3, column = 0, padx = 5,pady =5)
    mandatory_function_button = Button(text="Добавить", command=lambda : scene.add_mandatory_function(mandatory_function_entry.get()))
    mandatory_function_button.grid(row = 3, column = 2,padx=5, pady=5,sticky="e")

    start_code_entry = ScrolledText()
    start_code_entry.grid(row=4, column=1, padx=5, pady=5)
    if scene.get_start_code!="":
        start_code_entry.insert(0,scene.get_start_code)
    start_code_label = Label(text="Начальный код:")
    start_code_label.grid(row=4,column = 0,padx =5,pady=5)

    start_code_button = Button(text="Добавить",
                                       command=lambda: scene.set_start_code(start_code_entry.get("1.0",END)))
    start_code_button.grid(row=4, column=2, padx=5, pady=5, sticky="e")

    show_info_button.grid(row=5,column = 2,padx=5, pady=5,sticky="e")
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
    tapok = pygame.image.load("tapok.jpg").convert()
    tapok = pygame.transform.scale(tapok,(30,30))
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
                if event.key==pygame.K_m:
                    change_type = "mud"
                if event.key==pygame.K_e:
                    change_type="enemy"
                if event.key==pygame.K_a:
                    scene = Additional_Settings(scene)
                #print("Enemies:"+str(scene.get_enemies))
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
                    scene.remove_mud_cell(column,row)
                    scene.remove_enemy(column,row)
                    if scene.get_finish==(column,row):
                        scene.set_finish(-1,-1)
                    if scene.get_start==(column,row):
                        scene.set_start(-1,-1)
                if change_type=="treat":
                    scene.add_treat(column,row)
                if change_type=="mud":
                    scene.add_mud_cell(column,row)
                if change_type=="enemy":
                    scene.add_enemy(column,row,input_text("Тип врага:"))
        for i in range(size[1]):
            for j in range(size[0]):
                color = (255,255,255)
                if (j,i)in scene.get_blocked:
                    color = (0,0,255)
                elif (j,i)==scene.get_start:
                    color=(0,200,0)
                elif (j,i)==scene.get_finish:
                    color=(255,215,0)
                elif (j,i) in scene.get_mud_cells:
                    color = (205,133,63)
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * j + MARGIN,
                                  (MARGIN + HEIGHT) * i + MARGIN,
                                  WIDTH,
                                  HEIGHT])
                if (j,i) in scene.get_treats:
                    screen.blit(load_treat,((MARGIN + WIDTH) * j + MARGIN,(MARGIN + HEIGHT) * i + MARGIN))
                for k in scene.get_enemies:
                    if k['coords'] == (j, i):
                        screen.blit(tapok,
                                    ((MARGIN + WIDTH) * j + MARGIN,
                                     (MARGIN + HEIGHT) * i + MARGIN))
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