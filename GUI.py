from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice, QMimeData,
        QPoint, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty,
        QParallelAnimationGroup, QSequentialAnimationGroup)
from PyQt5.QtGui import QColor, QDrag, QPainter, QPixmap, QPainterPath
from PyQt5.QtWidgets import (QMainWindow, QApplication, QInputDialog , QFrame, QHBoxLayout,
    QVBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget)

from drawer import *
import re
import os

class QtStar(QLabel):
    def __init__(self, star, constellation, parent=None):
        color = Drawer.get_color(star)
        self.radius = Drawer.get_radius(star)

        self.pixmap = QPixmap('small_pic/{}_{}_round.png'.format(5, color)).scaled(self.radius, self.radius)
        # self.dark_pixmap = QPixmap('small_pic/{}_{}_dark.png'.format(radius, 'white'))
        self.dark_pixmap = QPixmap('small_pic/{}_{}_round.png'.format(5, 'white_dark')).scaled(self.radius, self.radius)

        self.star = star
        self.constellation = constellation
        super(QLabel, self).__init__(parent)
        self.setPixmap(self.dark_pixmap)
        self.coords = Geom.get_image_coords(star, 800, 0, 0)
        self.move(*self.coords)

        self.resize(self.radius + 10, self.radius + 10)
        # self.setToolTip(self.constellation.name+'\n'+str(self.coords))
        self.setToolTip(self.constellation.name)

    def enterEvent(self, event):
        print('mouseEnterEvent')
        for s in self.constellation.stars:
            s.setPixmap(s.pixmap)

    def leaveEvent(self, event):
        for s in self.constellation.stars:
            s.setPixmap(s.dark_pixmap)

class QtConstellation:
    def __init__(self, text, name, qtstars_parent):
        self.name = name
        lines = text.splitlines()
        self.stars = []
        for l in lines:
            star = Star(l)
            self.stars.append(QtStar(star, self, qtstars_parent))

    def get_constellations(qtstars_parent):
        path = './data/'
        txt_files = [x for x in os.listdir(path) if x.endswith('.txt')]


        # stars = []
        for name in txt_files:
            with open(path + name) as f:
                constellation = QtConstellation(f.read(), name[:-4], qtstars_parent)
                yield constellation


class StarsViewer(QFrame):
    def __init__(self, parent):
        super(StarsViewer, self).__init__(parent)
        self.setStyleSheet('background-color:black;')
        self.setMinimumSize(800, 800)
        self.setMaximumSize(800, 800)
        self.setMouseTracking(True)

        self.stars = []
        self.constellations = QtConstellation.get_constellations(self)
        for c in self.constellations:
            for s in c.stars:
                s.show()
                self.stars.append(s)

        self.changed_constellation = None

        self._view_coef = 1

    @property
    def view_coef(self):
        return self._view_coef

    @view_coef.setter
    def view_coef(self, value):
        self._view_coef = max(1, value)

    def mousePressEvent(self, event):
        print('mousePressEvent')
        child = self.childAt(event.pos())
        if not child:
            return

        self.changed_stars = []
        self.changed_constellation = child.constellation
        for s in self.changed_constellation.stars:
            s.setPixmap(QPixmap('small_pic/6_white_round2.png'))


    def mouseReleaseEvent(self, event):
        print('mouseReleaseEvent')
        if self.changed_constellation:
            for s in self.changed_constellation.stars:
                s.setPixmap(s.dark_pixmap)


    def wheelEvent(self, event):
        print('wheelEvent')
        if event.angleDelta().y() > 0:
            self.view_coef += 0.5
        else:
            self.view_coef -= 0.5

        for s in self.stars:
            new_coords = Geom.get_resize_image_coords(s.coords, 800, self.view_coef)
            # s.coords = new_coords
            # s.move(*self.coords)
            s.move(*new_coords)


    def get_dist00(coords, other_point):
        x_dist = abs(other_point[0] - coords[0])
        y_dist = abs(other_point[1] - coords[1])
        # square view
        # return max(x_dist, y_dist)

        # round view
        dist = sqrt(x_dist ** 2 + y_dist ** 2)
        return dist


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.star_viewer = StarsViewer(self)

        self.setMinimumSize(860, 900)
        # self.setMaximumSize(800, 900)

        self.setStyleSheet('background-color:black;')
        self.create_widgets()
        self.setLayout(self.get_layout())
        # self.change_view()
        # print(self.viewer.picture)


    def change_view(self, delta_ra, delta_dec):
        for s in self.star_viewer.stars:
            s.star.ra.full_sec += delta_ra
            s.star.dec.full_sec += delta_dec
            s.coords = Geom.get_image_coords(s.star, 800, 0, 0)
            s.coords = Geom.get_resize_image_coords(s.coords, 800, self.star_viewer.view_coef)
            s.move(*s.coords)

            s.setToolTip(s.constellation.name)


    def turn(self, side):
        c = 2
        if side == 'right':
            delta = (360*c, 0)
        elif side == 'left':
            delta = (-360*c, 0)
        elif side == 'up':
            delta = (0, -3600*c)
        elif side == 'down':
            delta = (0, 3600*c)

        self.change_view(*delta)



    def create_widgets(self):
        self.btn_left = QtWidgets.QToolButton()
        self.btn_left.setText('ᐊ')
        self.btn_left.setStyleSheet('color: white; background-color: black;') # dark-grey "#ff423e50"
        self.btn_left.clicked.connect(lambda: self.turn('left'))

        self.btn_right = QtWidgets.QToolButton(self)
        self.btn_right.setText('ᐅ')
        self.btn_right.setStyleSheet('color: white; background-color: black;')
        self.btn_right.clicked.connect(lambda: self.turn('right'))

        self.btn_up = QtWidgets.QToolButton()
        self.btn_up.setText('ᐃ')
        self.btn_up.setStyleSheet('color: white; background-color: black;')
        self.btn_up.clicked.connect(lambda: self.turn('up'))

        self.btn_down = QtWidgets.QToolButton()
        self.btn_down.setText('ᐁ')
        self.btn_down.setStyleSheet('color: white; background-color: black;')
        self.btn_down.clicked.connect(lambda: self.turn('down'))


    def get_layout(self):
        hbox0 = QtWidgets.QHBoxLayout()
        hbox0.addStretch()
        hbox0.addWidget(self.btn_left)
        hbox0.addSpacing(30)
        # hbox0.addWidget(self.btn_down)
        hbox0.addWidget(self.btn_right)
        hbox0.addSpacing(4)


        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(self.btn_up)
        hbox1.addSpacing(35)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch()
        hbox2.addSpacing(85)
        hbox2.addWidget(self.btn_down)
        hbox2.addSpacing(35)

        hbox3 = QtWidgets.QHBoxLayout()
        # hbox3.addStretch()
        hbox3.addWidget(self.star_viewer)
        # hbox3.addSpacing(35)

        vbox = QtWidgets.QVBoxLayout()
        # vbox.addStretch()
        # vbox.addSpacing(-900)
        # vbox.addWidget(self.star_viewer)

        vbox.addLayout(hbox3)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox2)
        return vbox


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # window.showMaximized()
    window.show()
    sys.exit(app.exec_())