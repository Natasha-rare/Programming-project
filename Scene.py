class Scene:
    def __init__(self):
        self.__size = (10,10)
        self.__blocked_cells = []
        self.__start = (0,0)
        self.__finish = (10,10)
        self.__entities = []
        self.__background_color = "White"
    def set_size(self,x,y):
        if (x==0 and y ==0) or (x<0 or y<0):
            raise Exception("Invalid scene size")
        self.__size = (x,y)
    def block_cell(self,x,y):#Блокирует клетку
        self.__blocked_cells.append((x,y))
    def unblock_cell(self,x,y):#Удаляет заблок. клетку. Если клетка удалилась возвращает True, иначе False
        for i in len(self.__blocked_cells):
            x_real,y_real,type = self.__blocked_cells[i]
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
    def get_start(self):#Возвращает точку старта.
        return  self.__start
    def get_finish(self):#Возваращает точку финиша.
        return  self.__finish
    def get_entities(self):#Возвращает суещств на сцене.
        return self.__entities
    def get_size(self):#Возвращает размер сцены.
        return self.__size

