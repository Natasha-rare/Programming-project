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
        self.__entities = []#существа|существо на сцене
        self.__player = Player(self)
        self.__background_color = "White"#цвет заднего плана
        self.__text = "SampleText"#текст задания
        #self.__mandatory_functions = []#функции обязательные для использования при выполнении задания
        self.__forbidden_functions = []#функции запрещенные для использования при выполнении задания
        self.__treats_cells = []#клетки с едой/наградами для сбора.
    def set_size(self,x,y):#Устанавливает размер сцены, если сцена меньше чем одна клетка, то вызывает исключение.
        if (x==0 and y ==0) or (x<0 or y<0):
            raise Exception("Invalid scene size")
        self.__size = (x,y)
    def block_cell(self,x,y):#Блокирует клетку, если на этой клетке находится старт, то клетку нельзя заблокировать.
        if self.__start==(x,y):
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
    def add_entity(self,x,y,entity):#Добавляет существо на сцену. Если другое существо уже есть на этих координатах или клетка заблокирована, то возвращает False, иначе True.
        for i in self.__entities:
            if i[0]==x and i[1]==y:
                return False
        if (x,y) in self.__blocked_cells:
            return False
        self.__entities.append(x,y,entity)
        return True
    def add_treat(self,x,y):#добавляет награду на клетку.
        self.__treats_cells.append((x,y))
    def remove_treat(self,x,y):#удаляет награду с клетки. Если не удалось удалить то False, иначе True.
        for i in range(len(self.__treats_cells)):
            x_real, y_real = self.__treats_cells[i]
            if x_real == x and y_real == y:
                self.__treats_cells.pop(i)
                return True
        return False
    def Solve_Code_Safe(self,code):
        future = self.Solve_Code(code)
        try:
            result = future.result()

            return result
        except Exception as error:
            return error
    @concurrent.process(timeout=6)
    def Solve_Code(self,code):#Решает код предоставленный пользователем и смотрит прошел пользователь задачу или нет.
                            # Вовзвращает шаги улитки пользователя, список собранных наград и прошел пользователь уровень или нет. Формат такой: {steps:[],treats:[],passed:Bool,errors:[]}
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
            errors.append('SystemError:'+str(e))
        passed = False
        if len(snail.get_steps) ==0 or snail.get_steps[-1]!=self.get_finish:
            errors.append("Not_On_Finish_Point")  # Добавляет ошибку, указывающую на то, что игрок не достиг финиша.
        for i in self.__forbidden_functions:
            if i in code:
                errors.append("Use_Of_Forbidden_Function:"+i)#Добавляет ошибку, указывающую на то, что игрок использовал запещенную функцию.
        if len(errors)==0:
            passed=True
        return {"steps":snail.get_steps,"treats":snail.get_collected,"passed":passed,"errors":errors}
    @property
    def get_start(self):#Возвращает точку старта.
        return  self.__start
    @property
    def get_finish(self):#Возваращает точку финиша.
        return  self.__finish
    @property
    def get_entities(self):#Возвращает суещств на сцене.
        return self.__entities
    @property
    def get_size(self):#Возвращает размер сцены.
        return self.__size
    @property#Вовзвращает массив кортежей заблокированных клеток.
    def get_blocked(self):
        return self.__blocked_cells
    @property
    def get_treats(self):
        return self.__treats_cells
class Player:
    def __init__(self,scene):
        self.__steps = []  # список точек передвжиения улитки.(массив кортежей координат (x,y))
        self.__scene = scene#Объект сцены на которой находится игрок.
        self.__position = scene.get_start
        self.__rotation = 90#угол поворота игрока в градусах, можно будет менять спрайт в зависимости от этого параметра. По дефолту поворот 90 градусов, значит улитка смотрит туда ----->
        self.__collected = []#массив кортежей (x,y), указывающий точки в которых пользователь подобрал награды
        self.__hp = 100#количество здоровья в процентах, не уверен, что будем убивать улиток в детской игре, но все же может пригодиться.

    def __go_to(self,x,y):#служебная функция для перехода на данные координаты
        if (x,y) in self.__scene.get_blocked or x<0 or y<0 or y>self.__scene.get_size[1]-1 or x>self.__scene.get_size[0]-1:
            return False
        self.__position = (x,y)
        self.__steps.append((x,y))
        return True
    def collect(self):#Собирает с клетки на которой стоит награду, если награды нет, то возвращает False, иначе True.
        if self.__position in self.__scene.get_treats:
            self.__collected.append(self.__position)
            self.__scene.remove_treat(self.__position[0],self.__position[1])
            return True
        return False
    @property
    def get_collected(self):#Возвращает массив кортежей (x,y), указывающий точки в которых пользователь подобрал награды
        return self.__collected
    def turn_left(self):#поворачивает игрока на 90 градусов влево
        self.__rotation-=90
        if self.__rotation<0:
            self.__rotation+=360
    def turn_right(self):#поворачивает игрока на 90 градусов вправо
        self.__rotation+=90
        if self.__rotation>=360:
            self.__rotation-=360
    def go_forward(self):#Сделать 1 шаг вперёд
        x = self.__position[0]
        y = self.__position[1]
        if self.__rotation==0:
            self.__go_to(x,y+1)
        if self.__rotation ==90:
            self.__go_to(x+1,y)
        if self.__rotation==180:
            self.__go_to(x,y-1)
        if self.__rotation==270:
            self.__go_to(x-1,y)
    @property
    def get_steps(self):
        return self.__steps