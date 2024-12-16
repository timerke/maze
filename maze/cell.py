from PyQt5.QtCore import QPointF


class Cell:
    """
    Класс для ячейки.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        :param x: горизонтальная координата;
        :param y: вертикальная координата.
        """

        self.parent = None
        self.x: int = x
        self.y: int = y
        self.g = 0  # Расстояние от начального узла до текущего узла
        self.h = 0  # Примерное расстояние от текущего узла до конечного узла
        self.f = 0  # Сумма g и h

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __lt__(self, other) -> bool:
        return self.f < other.f

    @property
    def point(self) -> QPointF:
        """
        :return: координата ячейки.
        """

        return QPointF(self.x, self.y)
