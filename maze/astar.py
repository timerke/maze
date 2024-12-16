import heapq
import math
import time
from typing import List
from PyQt5.QtCore import pyqtSignal, QThread
from .cell import Cell
from .maze import Maze


class AStar(QThread):

    final_path_signal: pyqtSignal = pyqtSignal(list)

    def __init__(self, maze: Maze) -> None:
        super().__init__()
        self._is_alive: bool = True
        self._is_running: bool = False
        self._maze: Maze = maze

    def _get_neighbors(self, cell: Cell) -> List[Cell]:
        neighbors = []
        for y in range(cell.y - 1, cell.y + 2):
            for x in range(cell.x - 1, cell.x + 2):
                if x == cell.x and y == cell.y or not self._maze.check_valid_position(x, y):
                    continue

                neighbors.append(Cell(x, y))

        return neighbors

    def _send_path(self, cell: Cell) -> List[Cell]:
        """
        :return: путь от заданной ячейки до исходной.
        """

        path = []
        while cell is not None:
            path.append(cell)
            cell = cell.parent

        self.final_path_signal.emit(path[::-1])

    def _run_astar(self) -> None:
        print("START")
        closed_cells = set()
        open_cells = []
        heapq.heappush(open_cells, self._maze.start_cell)
        while open_cells:
            current_cell = heapq.heappop(open_cells)  # Извлекаем ячейку с наименьшей оценкой f

            if current_cell == self._maze.finish_cell:
                self._send_path(current_cell)
                return

            closed_cells.add((current_cell.x, current_cell.y))
            neighbors = self._get_neighbors(current_cell)

            for neighbor in neighbors:
                if (neighbor.x, neighbor.y) in closed_cells:
                    continue

                # Вычисляем расстояние от начального узла до соседнего узла
                new_g = current_cell.g + 1

                # Если соседний узел уже находится в очереди с приоритетами
                for cell in open_cells:
                    if cell == neighbor:
                        old_neighbor = neighbor
                        break
                else:
                    old_neighbor = None

                if old_neighbor:
                    # Если новое расстояние до соседнего узла меньше, чем старое, обновляем значения g, h и f
                    if new_g < old_neighbor.g:
                        old_neighbor.g = new_g
                        old_neighbor.h = math.sqrt((self._maze.finish_cell.x - old_neighbor.x) ** 2 +
                                                   (self._maze.finish_cell.y - old_neighbor.y) ** 2)
                        old_neighbor.f = old_neighbor.g + old_neighbor.h
                        old_neighbor.parent = current_cell
                        # Обновляем приоритет соседнего узла в очереди с приоритетами
                        heapq.heapify(open_cells)
                else:
                    # Иначе добавляем соседний узел в очередь с приоритетами и вычисляем значения g, h и f
                    neighbor.g = new_g
                    neighbor.h = math.sqrt((self._maze.finish_cell.x - neighbor.x) ** 2 +
                                           (self._maze.finish_cell.y - neighbor.y) ** 2)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_cell
                    heapq.heappush(open_cells, neighbor)
        print("FINISH")

    def find_path(self) -> None:
        self._is_running = True

    def run(self) -> None:
        while self._is_alive:
            if self._is_running:
                self._run_astar()
                self._is_running = False

            time.sleep(0.5)

    def stop(self) -> None:
        self._is_alive = False
