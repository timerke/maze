import heapq
import math
import time
from typing import List, Optional, Set
from PyQt5.QtCore import pyqtSignal, QPointF, QThread
from .cell import Cell
from .maze import Maze


class AStar(QThread):
    """
    Класс, в котором происходит поиск выхода из лабиринта методом A*.
    """

    SLEEP_TIME_S: float = 0.01
    TIMEOUT_S: float = 0.1
    current_cell_signal: pyqtSignal = pyqtSignal(Cell)
    final_path_signal: pyqtSignal = pyqtSignal(list)
    neighbor_cell_signal: pyqtSignal = pyqtSignal(Cell)

    def __init__(self, maze: Maze) -> None:
        """
        :param maze: объект, в котором хранятся основные данные лабиринта.
        """

        super().__init__()
        self._closed_cells: Set[QPointF] = set()
        self._is_alive: bool = True
        self._is_running: bool = False
        self._maze: Maze = maze
        self._open_cells: List[Cell] = []

    def _add_new_cell(self, cell: Cell, new_g: int, current_cell: Cell) -> None:
        """
        Добавляем соседний узел в очередь с приоритетами и вычисляем значения g, h и f.
        :param cell: ячейка, которую нужно добавить в очередь с приоритетами;
        :param new_g:
        :param current_cell: текущая ячейка, которая является родительской.
        """

        cell.g = new_g
        cell.h = math.sqrt((self._maze.finish_cell.x - cell.x) ** 2 + (self._maze.finish_cell.y - cell.y) ** 2)
        cell.f = cell.g + cell.h
        cell.parent = current_cell
        heapq.heappush(self._open_cells, cell)
        self.neighbor_cell_signal.emit(cell)

    @staticmethod
    def _create_path_for_final_cell(cell: Optional[Cell] = None) -> List[Cell]:
        """
        :param cell: финальная ячейка, до которой нужно построить путь.
        :return: список из ячеек до финальной ячейки.
        """

        path = []
        while cell is not None:
            path.append(cell)
            cell = cell.parent

        return path[::-1]

    def _get_neighbors(self, cell: Cell) -> List[Cell]:
        """
        :param cell: ячейка, для которой нужно вернуть соседние ячейки.
        :return: список соседних ячеек.
        """

        neighbors = []
        for y in range(cell.y - 1, cell.y + 2):
            for x in range(cell.x - 1, cell.x + 2):
                if (x == cell.x and y == cell.y or (x != cell.x and y != cell.y) or (x, y) in self._closed_cells or
                        not self._maze.check_valid_position(x, y)):
                    continue

                neighbors.append(Cell(x, y))

        return neighbors

    def _run_astar(self) -> None:
        self._closed_cells = set()
        self._open_cells = []
        heapq.heappush(self._open_cells, self._maze.start_cell)

        while self._open_cells:
            current_cell = heapq.heappop(self._open_cells)  # Извлекаем ячейку с наименьшей оценкой f
            self.current_cell_signal.emit(current_cell)

            if current_cell == self._maze.finish_cell:
                self._send_path(current_cell)
                return

            self._closed_cells.add((current_cell.x, current_cell.y))
            neighbors = self._get_neighbors(current_cell)
            for neighbor in neighbors:
                self._update_open_cells(current_cell, neighbor)

            time.sleep(AStar.SLEEP_TIME_S)

        self._send_path()

    def _send_path(self, cell: Optional[Cell] = None) -> None:
        """
        Метод отправляет путь из лабиринта.
        :param cell: финальная ячейка из лабиринта.
        """

        path = self._create_path_for_final_cell(cell)
        self.final_path_signal.emit(path)

    def _update_old_cell(self, cell: Cell, new_g: int, current_cell: Cell) -> None:
        """
        :param cell: ячейка, которую нужно обновить в очереди с приоритетами;
        :param new_g:
        :param current_cell: текущая ячейка, которая является родительской.
        """

        # Если новое расстояние до соседнего ячейки меньше, чем старое, обновляем значения g, h и f
        cell.g = new_g
        cell.h = math.sqrt((self._maze.finish_cell.x - cell.x) ** 2 + (self._maze.finish_cell.y - cell.y) ** 2)
        cell.f = cell.g + cell.h
        cell.parent = current_cell
        # Обновляем приоритет соседней ячейки в очереди с приоритетами
        heapq.heapify(self._open_cells)

    def _update_open_cells(self, current_cell: Cell, neighbor: Cell) -> None:
        """
        :param current_cell: текущая ячейка;
        :param neighbor: соседняя ячейка, которую нужно добавить в очередь с приоритетами.
        """

        # Вычисляем расстояние от начального узла до соседнего узла
        new_g = current_cell.g + 1

        # Если соседний узел уже находится в очереди с приоритетами
        for cell in self._open_cells:
            if cell == neighbor and new_g < neighbor.g:
                self._update_old_cell(cell, new_g, current_cell)
                return

        self._add_new_cell(neighbor, new_g, current_cell)

    def find_path(self) -> None:
        self._is_running = True

    def run(self) -> None:
        while self._is_alive:
            if self._is_running:
                self._run_astar()
                self._is_running = False

            time.sleep(AStar.TIMEOUT_S)

    def stop(self) -> None:
        self._is_alive = False
