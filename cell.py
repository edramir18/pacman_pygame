from enum import Enum


class Cell:
    class CellType(Enum):
        WALL = '#'
        FLOOR = ' '

        def __str__(self):
            return str(self.value)

        def __repr__(self):
            return self.__str__()

    def __init__(self):
        self.celltype = Cell.CellType.WALL

    def __str__(self):
        return str(self.celltype)

    def __repr__(self):
        return self.__str__()

    def is_wall(self):
        return self.celltype == Cell.CellType.WALL

    def is_floor(self):
        return self.celltype == Cell.CellType.FLOOR

    def clone(self, other):
        if isinstance(other, Cell):
            self.celltype = other.celltype
        else:
            raise ValueError
