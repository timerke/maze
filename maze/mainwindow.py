import os
from typing import List
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from . import utils as ut
from .astar import AStar
from .cell import Cell
from .maze import Maze
from .mazewidget import MazeWidget


class MainWindow(QMainWindow):
    """
    Класс с основным окном приложения.
    """

    def __init__(self) -> None:
        super().__init__()
        self._maze: Maze = Maze()
        self._init_ui()
        self._create_astar()

    def _connect_buttons(self) -> None:
        self.button_find_way_out_of_maze.clicked.connect(self.find_way_out_of_maze)
        self.button_open_file.clicked.connect(self.open_file)

    def _create_astar(self) -> None:
        self._astar: AStar = AStar(self._maze)
        self._astar.current_cell_signal.connect(self._maze_widget.set_current_cell)
        self._astar.final_path_signal.connect(self._show_path)
        self._astar.neighbor_cell_signal.connect(self._maze_widget.set_neighbor_cell)
        self._astar.start()

    def _create_maze_widget(self) -> None:
        self._maze_widget: MazeWidget = MazeWidget(self._maze)
        self.layout_maze.addWidget(self._maze_widget)

    def _init_ui(self) -> None:
        loadUi(os.path.join("resources", "mainwindow.ui"), self)
        self._connect_buttons()
        self._create_maze_widget()

    @pyqtSlot(list)
    def _show_path(self, path: List[Cell]) -> None:
        """
        :param path: список ячеек, образующих выход из лабиринта.
        """

        if path:
            self._maze.set_path(path)
            self._maze_widget.show_path()
            ut.show_message("Информация", "Выход из лабиринта найден.")
        else:
            ut.show_message("Информация", "Не удалось найти выход из лабиринта.")

    @pyqtSlot()
    def find_way_out_of_maze(self) -> None:
        self._maze_widget.update_maze()
        self._astar.find_path()

    @pyqtSlot()
    def open_file(self) -> None:
        file_name = QFileDialog.getOpenFileName(self, "Открыть файл", ".", "Текстовые файлы (*.txt *.dat)")[0]
        if file_name:
            self._maze.read_maze_from_file(file_name)
            self._maze_widget.update_maze()
