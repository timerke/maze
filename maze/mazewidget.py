from typing import Optional
from PyQt5.QtCore import QLineF, QPointF, QRectF, QSizeF, Qt
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGraphicsView
from . import utils as ut
from .cell import Cell
from .maze import Maze


class MazeWidget(QGraphicsView):
    """
    Виджет для отображения лабиринта.
    """

    def __init__(self, maze: Maze) -> None:
        """
        :param maze: объект, в котором хранятся основные данные лабиринта.
        """

        super().__init__()
        self._current_cell: Optional[QRectF] = None
        self._maze: Maze = maze
        self.setScene(QGraphicsScene())
        self._set_view_parameters()
        self._create_brushes_and_pens()

    def _create_brushes_and_pens(self) -> None:
        self._border_pen: QPen = QPen(QBrush(QColor("black")), 2, Qt.SolidLine)
        self._border_pen.setCosmetic(True)

        self._current_pen: QPen = QPen(QBrush(QColor("yellow")), 2, Qt.SolidLine)
        self._current_pen.setCosmetic(True)

        self._finish_cell_brush: QBrush = QBrush(QColor("red"))
        self._finish_cell_pen: QPen = QPen(self._finish_cell_brush, 2, Qt.SolidLine)
        self._finish_cell_pen.setCosmetic(True)

        self._line_pen: QPen = QPen(QBrush(QColor("blue")), 2, Qt.SolidLine)
        self._line_pen.setCosmetic(True)

        self._neighbor_pen: QPen = QPen(QBrush(QColor("purple")), 2, Qt.SolidLine)
        self._neighbor_pen.setCosmetic(True)

        self._obstacle_brush: QBrush = QBrush(QColor("gray"))
        self._obstacle_pen: QPen = QPen(self._obstacle_brush, 2, Qt.SolidLine)
        self._obstacle_pen.setCosmetic(True)

        self._start_cell_brush: QBrush = QBrush(QColor("green"))
        self._start_cell_pen: QPen = QPen(self._start_cell_brush, 2, Qt.SolidLine)
        self._start_cell_pen.setCosmetic(True)

        self._path_pen: QPen = QPen(QBrush(QColor("orange")), 2, Qt.SolidLine)
        self._path_pen.setCosmetic(True)

    def _draw_mesh(self) -> None:
        if self._maze.maze_boundaries:
            self.scene().addRect(self._maze.maze_boundaries, self._border_pen)
            for y in range(self._maze.y_size - 1):
                self.scene().addLine(QLineF(QPointF(-0.5, y + 0.5), QPointF(self._maze.x_size - 0.5, y + 0.5)),
                                     self._line_pen)

            for x in range(self._maze.x_size - 1):
                self.scene().addLine(QLineF(QPointF(x + 0.5, -0.5), QPointF(x + 0.5, self._maze.y_size - 0.5)),
                                     self._line_pen)

    def _draw_obstacles(self) -> None:
        for obstacle in self._maze.get_rects_for_obstacles():
            self.scene().addRect(obstacle, self._obstacle_pen, self._obstacle_brush)

    def _draw_start_and_finish_cells(self) -> None:
        finish_cell = self._maze.get_rect_for_finish_cell()
        if finish_cell:
            self.scene().addEllipse(finish_cell, self._finish_cell_pen, self._finish_cell_brush)

        start_cell = self._maze.get_rect_for_start_cell()
        if start_cell:
            self.scene().addEllipse(start_cell, self._start_cell_pen, self._start_cell_brush)

    def _fit_image(self) -> None:
        if self._maze.x_size is not None and self._maze.y_size is not None:
            self.fitInView(QRectF(QPointF(-1, -1), QSizeF(self._maze.x_size + 1, self._maze.y_size + 1)),
                           Qt.AspectRatioMode.KeepAspectRatio)

    def _set_view_parameters(self) -> None:
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameShape(QFrame.NoFrame)
        self.setMouseTracking(True)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def set_current_cell(self, cell: Cell) -> None:
        if self._current_cell:
            self._current_cell.setPen(self._neighbor_pen)

        rect = ut.get_rect_for_cell(cell, Maze.POINT_SIZE)
        self._current_cell = self.scene().addEllipse(rect, self._current_pen)

    def set_neighbor_cell(self, cell: Cell) -> None:
        rect = ut.get_rect_for_cell(cell, Maze.POINT_SIZE)
        self.scene().addEllipse(rect, self._neighbor_pen)

    def show_path(self) -> None:
        for line in self._maze.get_lines_for_path():
            self.scene().addLine(line, self._path_pen)

    def update_maze(self) -> None:
        self.scene().clear()
        self._current_cell = None
        self._draw_mesh()
        self._draw_start_and_finish_cells()
        self._draw_obstacles()
        self._fit_image()
