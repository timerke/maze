from typing import List, Optional
from . import utils as ut
from .cell import Cell
from .point import Point


class Maze:
    """
    Класс для лабиринта.
    """

    def __init__(self) -> None:
        self._finish_cell: Optional[Cell] = None
        self._obstacles: List[Point] = []
        self._start_cell: Optional[Cell] = None
        self._x_size: Optional[int] = None
        self._y_size: Optional[int] = None

    def clear(self) -> None:
        self._finish_cell = None
        self._obstacles.clear()
        self._start_cell = None
        self._x_size = None
        self._y_size = None

    def read_maze_from_file(self, file_name: str) -> "Maze":
        """
        :param file_name: имя файла, в котором содержится карта лабиринта.
        :return: лабиринт на основе данных из файла.
        """

        self.clear()

        data = ut.read_file(file_name)
        for y, line in enumerate(data.split("\n")):
            for x, symbol in enumerate(line):
                symbol = symbol.lower()
                if symbol == "a":
                    self._start_cell = Cell(x, y)
                elif symbol == "b":
                    self._finish_cell = Cell(x, y)
                elif symbol == "*":
                    self._obstacles.append(Point(x, y))

            if self._x_size is None or len(line) > self._x_size:
                self._x_size = len(line)

            self._y_size = y
