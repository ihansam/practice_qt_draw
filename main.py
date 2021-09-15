import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QColor
import main_ui
import dialog
from typing import List


class Figure:
    def __init__(self, typ: str, lyr: str, coord: List[float]):
        self.type = typ
        self.layer = lyr
        self.coordinates = coord

    def __str__(self):
        return f"{self.type}:{self.layer}:{self.coordinates}"


def is_valid(obj: list) -> bool:
    try:
        typ = obj[0]
        coord = obj[2:]
        if typ == "rectangle":
            if len(coord) != 4:
                return False
        elif typ == "polygon":
            if len(coord) % 2 != 0:
                return False
        else:
            return False

        for number in coord:
            tmp = float(number)

        return True

    except IndexError or ValueError:
        return False


def convert(string: str) -> List[Figure]:
    figs = []
    objects = [obj.split(',') for obj in string.split('\n')]

    for obj in objects:
        if is_valid(obj):
            figs.append(Figure(obj[0], obj[1], list(map(float, obj[2:]))))
        else:
            figs.clear()
            figs.append(Figure("error", "", []))
            break

    return figs


def draw_rect(qp, color, coord):
    qp.setPen(QPen(QColor(*color), 2))
    qp.drawRect(*coord)


def draw_line(qp, color, coord):
    qp.setPen(QPen(QColor(*color), 2))
    qp.drawLine(*coord)


def draw(qp: QPainter, figs: List[Figure]) -> None:
    color_rgb = {'red': (255, 0, 0), 'green': (0, 0, 255), 'blue': (0, 0, 255), 'black': (0, 0, 0)}
    for figure in figs:
        if figure.type == "rectangle":
            draw_rect(qp, color_rgb[figure.layer], figure.coordinates)
        elif figure.type == "polygon":
            for i in range(0, len(figure.coordinates)-3, 2):
                draw_line(qp, color_rgb[figure.layer], [figure.coordinates[i+j] for j in range(4)])
        elif figure.type == "error":
            qp.drawText(300, 300, "Invalid Input")


class SubWindow(QDialog, dialog.Ui_Dialog, QMainWindow):
    def __init__(self, parent, input_txt):
        super().__init__(parent)
        self.show()
        self.setupUi(self)
        self.figures = convert(input_txt)

    def paintEvent(self, a0) -> None:
        qp = QPainter()
        qp.begin(self)
        draw(qp, self.figures)
        qp.end()


class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_show.clicked.connect(self.open_dialog)

    def open_dialog(self):
        input_text = self.plainTextEdit_input.toPlainText()
        SubWindow(self, input_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()
