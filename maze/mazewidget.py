from PyQt5.QtWidgets import QGraphicsView


class MazeWidget(QGraphicsView):
    """
    Виджет для отображения лабиринта.
    """

    def __init__(self) -> None:
        super().__init__()
