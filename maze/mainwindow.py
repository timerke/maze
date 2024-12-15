import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from . import utils as ut
from .mazewidget import MazeWidget


class MainWindow(QMainWindow):
    """
    Класс с основным окном приложения.
    """

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _connect_buttons(self) -> None:
        self.button_find_way_out_of_maze.clicked.connect(self.find_way_out_of_maze)
        self.button_open_file.clicked.connect(self.open_file)

    def _create_maze_widget(self) -> None:
        self._maze_widget: MazeWidget = MazeWidget()
        self.layout_maze.addWidget(self._maze_widget)

    def _init_ui(self) -> None:
        loadUi(os.path.join("resources", "mainwindow.ui"), self)
        self._connect_buttons()
        self._create_maze_widget()

    @pyqtSlot()
    def find_way_out_of_maze(self) -> None:
        print("Find way")

    @pyqtSlot()
    def open_file(self) -> None:
        file_name = QFileDialog.getOpenFileName(self, "Открыть файл", ".", "Текстовые файлы (*.txt *.dat)")[0]
        if file_name:
            ut.read_file(file_name)
