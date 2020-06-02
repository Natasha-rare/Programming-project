class Scene:
    def __init__(self):
        self.__size = (10,10)#размер поля в клетках
        self.__blocked_cells = []#заблокированные клетки
        self.__start = (0,0)#клетка старта
        self.__finish = (9,9)#клетка финиша
        self.__entities = []#существа|существо на сцене
        self.__background_color = "White"#цвет заднего плана
        self.__text = "SampleText"#текст задания
        self.__mandatory_functions = []#функции обязательные для использования при выполнении задания
        self.__forbidden_functions = []#функции запрещенные для использования при выполнении задания
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

    @property
    def get_blocked(self):
        return self.__blocked_cells


