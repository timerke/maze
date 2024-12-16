from PyQt5.QtCore import QPointF, QRectF
from .cell import Cell


def get_rect_for_cell(cell: Cell, size: float) -> QRectF:
    """
    :param cell: ячейка, которую нужно нарисовать;
    :param size:
    :return: прямоугольник для рисования заданной ячейки.
    """

    top_left = QPointF(cell.x - size / 2, cell.y - size / 2)
    bottom_right = QPointF(cell.x + size / 2, cell.y + size / 2)
    return QRectF(top_left, bottom_right)


def read_file(file_name: str) -> str:
    """
    :param file_name: имя файла, который нужно прочитать.
    :return: содержимое файла.
    """

    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()
