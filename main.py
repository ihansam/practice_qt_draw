import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QColor
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


def draw_a_rect(qp: QPainter, x1, x2, y1, y2):
    qp.setPen(QPen(QColor(255, 0, 0), 2))
    qp.drawRect(x1, x2, y1, y2)


def draw(qp: QPainter, figs: List[Figure]) -> None:
    for figure in figs:
        if figure.type == "rectangle":
            pass
        elif figure.type == "polygon":
            pass
        elif figure.type == "error":
            pass
    # test
    draw_a_rect(qp, 20, 20, 100, 100)
    draw_a_rect(qp, 180, 120, 50, 120)


class MyWindow(QMainWindow, dialog.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        figures_string = "rectangle,green,30.0,40.0,20.0,30.0\n" \
                         "rectangle,red,60.0,90.0,40.0,70.0\n" \
                         "polygon,black,10.0,20.0,30.0,40.0,80.0,20.0,10.0,20.0"
        self.figures = convert(figures_string)

    def paintEvent(self, a0) -> None:
        qp = QPainter()
        qp.begin(self)
        draw(qp, self.figures)
        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
