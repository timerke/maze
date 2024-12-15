from PyQt5.QtCore import QLineF, QPoint, QPointF, Qt
from PyQt5.QtGui import QBrush, QColor, QPen, QWheelEvent
from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGraphicsView
from .maze import Maze


class MazeWidget(QGraphicsView):
    """
    Виджет для отображения лабиринта.
    """

    MIN_SCALE: float = 0.1
    ZOOM_SPEED: float = 0.001

    def __init__(self, maze: Maze) -> None:
        """
        :param maze: объект с данными лабиринта.
        """

        super().__init__()
        self._maze: Maze = maze
        self._scale: float = 1
        self.setScene(QGraphicsScene())
        self._set_view_parameters()
        self._create_pens()

    def _create_pens(self) -> None:
        self._border_pen: QPen = QPen(QBrush(QColor("black")), 2, Qt.SolidLine)
        self._border_pen.setCosmetic(True)

        self._finish_point_brush: QBrush = QBrush(QColor("red"))
        self._finish_point_pen: QPen = QPen(self._finish_point_brush, 2, Qt.SolidLine)
        self._finish_point_pen.setCosmetic(True)

        self._line_pen: QPen = QPen(QBrush(QColor("blue")), 2, Qt.SolidLine)
        self._line_pen.setCosmetic(True)

        self._start_point_brush: QBrush = QBrush(QColor("green"))
        self._start_point_pen: QPen = QPen(self._start_point_brush, 2, Qt.SolidLine)
        self._start_point_pen.setCosmetic(True)

    def _draw_mesh(self) -> None:
        self.scene().addRect(self._maze.maze_boundaries, self._border_pen)
        for y in range(self._maze.y_size - 1):
            self.scene().addLine(QLineF(QPointF(-0.5, y + 0.5), QPointF(self._maze.x_size - 0.5, y + 0.5)), self._line_pen)

        for x in range(self._maze.x_size - 1):
            self.scene().addLine(QLineF(QPointF(x + 0.5, -0.5), QPointF(x + 0.5, self._maze.y_size - 0.5)), self._line_pen)

    def _draw_start_and_finish_points(self) -> None:
        self.scene().addEllipse(self._maze.finish_point, self._finish_point_pen, self._finish_point_brush)
        self.scene().addEllipse(self._maze.start_point, self._start_point_pen, self._start_point_brush)

    def _get_zoom_factor(self, event: QWheelEvent) -> float:
        """
        :param event: wheel event.
        :return: zoom factor.
        """

        zoom_factor = 1.0
        zoom_factor += event.angleDelta().y() * MazeWidget.ZOOM_SPEED
        return zoom_factor

    def _set_view_parameters(self) -> None:
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameShape(QFrame.NoFrame)
        self.setMouseTracking(True)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def update_maze(self) -> None:
        self.scene().clear()
        self._draw_mesh()
        self._draw_start_and_finish_points()

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        :param event: wheel event.
        """

        zoom_factor = self._get_zoom_factor(event)
        if self._scale * zoom_factor < MazeWidget.MIN_SCALE and zoom_factor < 1.0:
            return

        self.zoom(zoom_factor, event.pos())
        self._scale *= zoom_factor

    def zoom(self, zoom_factor: float, pos: QPoint) -> None:  # pos in view coordinates
        """
        :param zoom_factor: scale factor;
        :param pos:
        """

        old_scene_pos = self.mapToScene(pos)

        # Note: Workaround! See:
        # - https://bugreports.qt.io/browse/QTBUG-7328
        # - https://stackoverflow.com/questions/14610568/how-to-use-the-qgraphicsviews-translate-function
        anchor = self.transformationAnchor()
        self.setTransformationAnchor(QGraphicsView.NoAnchor)  # Override transformation anchor
        self.scale(zoom_factor, zoom_factor)
        delta = self.mapToScene(pos) - old_scene_pos
        self.translate(delta.x(), delta.y())
        self.setTransformationAnchor(anchor)  # Restore old anchor
