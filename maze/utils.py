import os
from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from .cell import Cell


def get_rect_for_cell(cell: Cell, size: float) -> QRectF:
    """
    :param cell: ячейка, которую нужно нарисовать;
    :param size: ширина и высота ячейки.
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


def show_message(title: str, text: str, icon: QMessageBox.Icon = QMessageBox.Information, additional_text: str = "",
                 detailed_text: str = "") -> None:
    """
    :param title: заголовок окна с сообщением;
    :param text: текст сообщения;
    :param icon: иконка окна с сообщением;
    :param additional_text:
    :param detailed_text:
    """

    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setWindowIcon(QIcon(os.path.join("resources", "icon.jpg")))
    message_box.setIcon(icon)
    message_box.setTextFormat(Qt.RichText)
    message_box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    message_box.setText(text)

    if additional_text:
        message_box.setInformativeText(additional_text)

    if detailed_text:
        message_box.setDetailedText(detailed_text)

    message_box.exec_()
