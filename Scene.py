class Scene:
    def __init__(self):
        self.__size = (10,10)
        self.__blocked_cells = []
        self.__start = (0,0)
        self.__finish = (10,10)
        self.__entities = []
        self.__background_color = "White"
    def block_cell(self,x,y,type = "Stone"):#Блокирует клетку одним из типов
        self.__blocked_cells.append((x,y,type))
    def unblock_cell(self,x,y):#Удаляет заблок. клетку. Если клетка удалилась возвращает True, иначе False
        for i in len(self.__blocked_cells):
            x_real,y_real,type = self.__blocked_cells[i]
            if x_real == x and y_real==y:
                self.__blocked_cells.pop(i)
                return True
        return False
    def set_start(self,x,y):#Устанавливает точку старта.
        self.__start = (x,y)
    def set_finish(self,x,y):#Устанавливает точку финиша.
        self.__finish = (x,y)
    def add_entity(self,x,y,entity):#Добавляет существо на сцену. Если другое существо уже есть на этих координатах, то возвращает False, иначе True.
        for i in self.__entities:
            if i[0]==x and i[1]==y:
                return False
        self.__entities.append(x,y,entity)
        return True

