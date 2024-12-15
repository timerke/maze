from typing import List, Optional
from PyQt5.QtCore import QPointF, QRectF, QSizeF
from . import utils as ut
from .cell import Cell
from .point import Point


class Maze:
    """
    Класс для лабиринта.
    """

    POINT_SIZE: float = 0.3

    def __init__(self) -> None:
        self._finish_cell: Optional[Cell] = None
        self._obstacles: List[Point] = []
        self._start_cell: Optional[Cell] = None
        self._x_size: Optional[int] = None
        self._y_size: Optional[int] = None

    @property
    def finish_point(self) -> QRectF:
        """
        :return:
        """

        return self._get_rect_for_cell(self._finish_cell)

    @property
    def start_point(self) -> QRectF:
        """
        :return:
        """

        return self._get_rect_for_cell(self._start_cell)

    @property
    def maze_boundaries(self) -> QRectF:
        """
        :return: границы лабиринта.
        """

        return QRectF(QPointF(-0.5, -0.5), QSizeF(self._x_size, self._y_size))

    @property
    def x_size(self) -> int:
        """
        :return: ширина лабиринта.
        """

        return self._x_size

    @property
    def y_size(self) -> int:
        """
        :return: высота лабиринта.
        """

        return self._y_size

    @staticmethod
    def _get_rect_for_cell(cell: Cell) -> QRectF:
        """
        :return:
        """

        top_left = QPointF(cell.x - Maze.POINT_SIZE / 2, cell.y - Maze.POINT_SIZE / 2)
        bottom_right = QPointF(cell.x + Maze.POINT_SIZE / 2, cell.y + Maze.POINT_SIZE / 2)
        return QRectF(top_left, bottom_right)

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
        lines = data.split("\n")
        self._y_size = len(lines)
        for y, line in enumerate(lines):
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
