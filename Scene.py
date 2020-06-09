from RestrictedPython import compile_restricted
from RestrictedPython import safe_globals
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.Guards import guarded_iter_unpack_sequence
from pebble import concurrent


class Scene:
    def __init__(self,size = (10,10)):
        self.__size = size#размер поля в клетках
        self.__blocked_cells = []#заблокированные клетки
        self.__start = (0,0)#клетка старта
        self.__finish = (9,9)#клетка финиша
        self.__enemies = []#враг|враги на сцене
        self.__player = Player(self)
        self.__background_color = "White"#цвет заднего плана
        self.__text = "SampleText"#текст задания
        self.__mud_cells = []#клетка, на прохождение которое потребуется не один “ход”, а два
        self.__player_step_limit = 99999#лимит на количество шагов игрока
        self.__mandatory_functions = []#функции обязательные для использования при выполнении задания
        self.__forbidden_functions = []#функции запрещенные для использования при выполнении задания
        self.__treats_cells = []#клетки с едой/наградами для сбора.
        self.__minimum_food_collected = 0#минимум еды собранной за уровень
        self.__limited_functions = []#Лимитированные функции-т.е могут быть использованы только n-ое кол-во раз
        self.__start_code = ""#Код который по дефолту задается учителем, данный код может менять только сам учитель при создании задания.
    def set_food_limit(self,amount):
        self.__minimum_food_collected=amount
    @property
    def get_food_limit(self,amount):
        return self.__minimum_food_collected
    def add_enemy(self,x,y,type):#Добавляет врага, если там уже есть другой враг, то возвращает False, иначе True
        for i in self.__enemies:
            if i['coords']==(x,y):
                return False
        self.__enemies.append({"coords":(x,y),"type":type})
        return True

    def remove_enemy(self,x,y):
       for i in range(len(self.__enemies)):
           if self.__enemies[i]['coords']==(x,y):
               self.__enemies.pop(i)
    @property
    def get_enemies(self):
        return self.__enemies
    def set_start_code(self,code):
        self.__start_code = code
        if self.__start_code!="" and self.__start_code[-1]!='\n':#делает последний символ в код переносом на новую строчку, т.к некоторые могут об этом забывать.
            self.__start_code+='\n'
    @property
    def get_start_code(self):
        return self.__start_code
    def add_mandatory_function(self,function):
        self.__mandatory_functions.append(function)
    def remove_mandatory_function(self,function):
        self.__mandatory_functions.remove(function)
    @property
    def get_mandatoy_functions(self):
        return self.__mandatory_functions
    def add_mud_cell(self,x,y):#добавляет грязевую клетку
        if (x,y) not in self.__mud_cells:
            self.__mud_cells.append((x,y))
    def remove_mud_cell(self,x,y):#удаляет грязевую клетку
        for i in self.__mud_cells:
            if i ==(x,y):
                self.__mud_cells.remove((x,y))

    def set_player_step_limit(self,amount):#устанавливает лимит на количество шагов игрока
        self.__player_step_limit = int(amount)
    def set_size(self,x,y):#Устанавливает размер сцены, если сцена меньше чем одна клетка, то вызывает исключение.
        if (x==0 and y ==0) or (x<0 or y<0):
            raise Exception("Invalid scene size")
        self.__size = (x,y)
    def block_cell(self,x,y):#Блокирует клетку, если на этой клетке находится старт, то клетку нельзя заблокировать.
        if self.__start==(x,y) or (x,y) in self.__blocked_cells:
            return False
        self.__blocked_cells.append((x,y))
        return True
    def unblock_cell(self,x,y):#Удаляет заблок. клетку. Если клетка удалилась возвращает True, иначе False
        for i in range(len(self.__blocked_cells)):
            x_real,y_real = self.__blocked_cells[i]
            if x_real == x and y_real==y:
                self.__blocked_cells.pop(i)
                return True
        return False
    def set_start(self,x,y):#Устанавливает точку старта, если точка заблокирована то возвращает False, иначе True
        if (x,y) in self.__blocked_cells:
            return False
        self.__start = (x,y)
        return True
    def set_finish(self,x,y):#Устанавливает точку финиша, если данная точка заблокирована, то возвращает False, иначе True
        if (x,y) in self.__blocked_cells:
            return False
        self.__finish = (x,y)
        return True
    def add_treat(self,x,y,amount,type="Leaf"):#добавляет награду на клетку.
        for i in self.__treats_cells:
            if i['coords']==(x,y):
                return False
        self.__treats_cells.append({"coords":(x,y),"amount":amount,"type":type})
        return True
    def remove_treat(self,x,y):#удаляет награду с клетки. Если не удалось удалить то False, иначе True.
        for i in self.__treats_cells:
            if i['coords']==(x,y):
                self.__treats_cells.remove(i)
                return True
        return False
    def add_forbiden_func(self,func_name):#добавляет функцию которую нельзя использовать в данной задаче
        self.__forbidden_functions.append(func_name)
    def add_limited_function(self,function_name,amount):#Добавляет лимит на использование функции с назанием function_name, т.е ее можно будет использовать только amount раз
        self.__limited_functions.append({"name":function_name,"amount_allowed":amount})
    def remove_limited_function(self,function_name):
        for i in range(len(self.__limited_functions)):
            if self.__limited_functions[i]['name']==function_name:
                self.__limited_functions.pop(i)
    # def Solve_Code_Docker(self,code):#Когда-нибудь у нас будет сервер на линуксе и мы это протестируем, но это будет не сейчас.
    #     code = "from Scene import *\n"+self.get_start_code+code
    #     epicbox.configure(
    #         profiles=[
    #             epicbox.Profile('python', 'python:3.6.5-alpine')
    #         ]
    #     )
    #     scene_source = open('Scene.py').read()
    #     files = [{'name': 'main.py', 'content': code.encode('utf-8')},{'name': 'Scene.py', 'content': scene_source.encode('utf-8')}]
    #     limits = {'cputime': 1, 'memory': 64}
    #     result = epicbox.run('python', 'python3 main.py', files=files, limits=limits)
    #     return result
    def Solve_Code_Safe(self,code):
        future = self.Solve_Code(self.get_start_code+code)
        try:
            result = future.result()

            return result
        except Exception as error:
            return error.__traceback__()
    @concurrent.process(timeout=6)
    def Solve_Code(self,code):#Решает код предоставленный пользователем и смотрит прошел пользователь задачу или нет.
                            # Вовзвращает шаги улитки пользователя, список собранных наград и прошел пользователь уровень или нет. Формат такой: {steps:[{type:"type",coords:(x,y),custom:{}}],treats:[],passed:Bool,errors:[]}
        #set_max_runtime(1)#Максимальное кол-во секунд действия процессора
        snail = self.__player

        byte_code = compile_restricted(code, '<string>', 'exec')
        safe_globals.update({"Scene":Scene,"snail":snail,"Player":Player})
        safe_globals['_getiter_'] = default_guarded_getiter
        safe_globals['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
        errors = []
        try:
            exec(byte_code,safe_globals,{})#{"Scene":Scene,"snail":snail,"Player":Player}
        except Exception as e:
            errors.append({'SystemError':str(e)})
        passed = False
        if len(snail.get_steps) ==0 or snail.get_position!=self.get_finish:
            errors.append({"Not_On_Finish_Point":True})  # Добавляет ошибку, указывающую на то, что игрок не достиг финиша.
        for i in self.__forbidden_functions:
            if i in code:
                errors.append({"Use_Of_Forbidden_Function":i})#Добавляет ошибку, указывающую на то, что игрок использовал запещенную функцию.
        for i in self.__limited_functions:
            if code.count(i['name'])>int(i['amount_allowed']):
                errors.append({"Exceeded_Limit_Of_Function":i['name']})
        for i in self.__mandatory_functions:
            if i not in code:
                errors.append({"UnusedMandatoryFunction": i})
        if snail.get_food_collected<self.__minimum_food_collected:
            errors.append({"NotEnoughFood":snail.get_food_collected})
        if len(errors)==0:
            passed=True
        #print("\n#res#\n"+{"steps":snail.get_steps,"treats":snail.get_collected,"passed":passed,"errors":errors,"scene":self.__player.get_scene})
        return {"steps":snail.get_steps,"treats":snail.get_collected,"food_collected":snail.get_food_collected,"passed":passed,"errors":errors,"scene":self.__player.get_scene}
    @property
    def get_player_pos(self):
        return self.__player.get_position
    @property
    def get_start(self):#Возвращает точку старта.
        return  self.__start
    @property
    def get_finish(self):#Возваращает точку финиша.
        return  self.__finish
    @property
    def get_enemies(self):#Возвращает врагов на сцене.
        return self.__enemies
    @property
    def get_size(self):#Возвращает размер сцены.
        return self.__size
    @property#Вовзвращает массив кортежей заблокированных клеток.
    def get_blocked(self):
        return self.__blocked_cells
    @property
    def get_treats(self):
        return self.__treats_cells
    @property
    def get_limited_functions(self):
        return self.__limited_functions
    @property
    def get_player_step_limit(self):
        return self.__player_step_limit
    @property
    def get_mud_cells(self):
        return self.__mud_cells
    @property
    def update_player(self):
        self.__player = Player(self)
class Player:
    def __init__(self,scene):
        self.__steps = []  # список действий улитки
        self.__scene = scene#Объект сцены на которой находится игрок.
        self.__position = scene.get_start
        self.__rotation = 90#угол поворота игрока в градусах, можно будет менять спрайт в зависимости от этого параметра. По дефолту поворот 90 градусов, значит улитка смотрит туда ----->
        self.__collected = []#массив кортежей (x,y), указывающий точки в которых пользователь подобрал награды
        self.__hp = 100#количество здоровья в процентах, не уверен, что будем убивать улиток в детской игре, но все же может пригодиться.
        self.__food_collected = 0#собрано еды
    @property
    def get_food_collected(self):
        return self.__food_collected
    def check_can_move(self,x1,y1,x2,y2):
        if (x1,y1) not in self.__scene.get_blocked:
            return False
        if (x2,y2) in self.__scene.get_blocked:
            return False
        for i in self.__scene.get_enemies:
            if i['coords'] == (x2, y2):
                return False
        if x2 < 0 or y2 < 0 or y2 > self.__scene.get_size[1] - 1 or x2 > self.__scene.get_size[0] - 1:
            return False
        return True

    def move_blocked(self):#позволяет двигать заблокированную клетку.
        x = self.__position[0]
        y = self.__position[1]
        if self.__rotation == 0 and self.check_can_move(x,y-1,x,y-2):

                self.__scene.unblock_cell(x, y - 1)
                self.__scene.block_cell(x, y - 2)
                self.__steps.append({"type": "moved_blocked", "coords": self.__position,"custom":[(x, y - 1),(x, y - 2)]})
        if self.__rotation == 90 and self.check_can_move(x+1,y,x+2,y):
                self.__scene.unblock_cell(x+1,y)
                self.__scene.block_cell(x+2,y)
                self.__steps.append({"type": "moved_blocked", "coords": self.__position, "custom": [(x+1, y), (x+2, y)]})
        if self.__rotation == 180 and self.check_can_move(x,y+1,x,y+2):

                self.__scene.unblock_cell(x, y+1)
                self.__scene.block_cell(x, y+2)
                self.__steps.append({"type": "moved_blocked", "coords": self.__position, "custom": [(x, y+1), (x, y+2)]})
        if self.__rotation == 270and self.check_can_move(x-1, y,x-2, y):

                self.__scene.unblock_cell(x-1, y)
                self.__scene.block_cell(x-2, y)
                self.__steps.append({"type": "moved_blocked", "coords": self.__position, "custom": [(x-1, y), (x-2, y)]})
    def __go_to(self,x,y):#служебная функция для перехода на данные координаты
        if (x,y) in self.__scene.get_blocked or x<0 or y<0 or y>self.__scene.get_size[1]-1 or x>self.__scene.get_size[0]-1:
            return False
        if self.get_steps_left==0 or ((x,y) in self.__scene.get_mud_cells and self.get_steps_left==1):
            raise Exception("OutOfGas")
        for i in self.__scene.get_enemies:
            if i['coords']==(x,y):
                self.__steps.append({"type": "got_killed", "coords": self.__position,"custom":i})#был убит врагом i при переходе с позиции coords на позицию врага.
                raise Exception("GotEaten")
        self.__steps.append({"type": "go_forward", "coords": self.__position,"custom":(x,y)})  # Формат {type:"type",coords:(x,y),custom:}
        self.__position = (x,y)

        self.__scene.set_player_step_limit(self.get_steps_left-1)
        if (x,y) in self.__scene.get_mud_cells:
            self.__scene.set_player_step_limit(self.get_steps_left - 1)
        return True
    def collect(self):#Собирает с клетки на которой стоит награду, если награды нет, то возвращает False, иначе True.

        for i in self.__scene.get_treats:
            if i['coords']==self.__position:
                self.__collected.append(self.__position)
                self.__scene.remove_treat(self.__position[0],self.__position[1])
                self.__food_collected+=i['amount']
                self.__steps.append({"type": "collect_treat", "coords": self.__position,"custom":self.get_food_collected})#Добавляет в результат действие сбора награды,координаты действия и количество собранных наград после выполнения выполнения.
                return True
        return False
    @property
    def get_collected(self):#Возвращает массив кортежей (x,y), указывающий точки в которых пользователь подобрал награды
        return self.__collected
    def turn_left(self):#поворачивает игрока на 90 градусов влево
        self.__rotation-=90

        if self.__rotation<0:
            self.__rotation+=360
        self.__steps.append({"type": "turn", "coords": self.__position,"custom": self.__rotation})  # Добавляет в результат действие поворота, в custom сохраняется значение поворота после выполения действия.
    def turn_right(self):#поворачивает игрока на 90 градусов вправо
        self.__rotation+=90
        if self.__rotation>=360:
            self.__rotation-=360
        self.__steps.append({"type": "turn", "coords": self.__position,"custom": self.__rotation})  # Добавляет в результат действие поворота, в custom сохраняется значение поворота после выполения действия.
    def go_forward(self):#Сделать 1 шаг вперёд
        x = self.__position[0]
        y = self.__position[1]
        if self.__rotation==0:
            self.__go_to(x,y-1)
        if self.__rotation ==90:
            self.__go_to(x+1,y)
        if self.__rotation==180:
            self.__go_to(x,y+1)
        if self.__rotation==270:
            self.__go_to(x-1,y)

    @property
    def get_steps(self):
        return self.__steps
    @property
    def get_rotation(self):
        return  self.__rotation
    @property
    def get_position(self):
        return self.__position
    @property
    def get_steps_left(self):
        return self.__scene.get_player_step_limit
    @property
    def get_scene(self):
        return self.__scene