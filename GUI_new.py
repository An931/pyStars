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
    def __init__(self, star, parent=None):
        # star = Star(line)
        pixmap = QPixmap('small_pic/1_white.png')
        # pixmap = QPixmap('small_pic/10_green.png'.format(color[0]+'_'+name))
        super(QLabel, self).__init__(parent)
        self.setPixmap(pixmap)
        self.coords = Geom.get_image_coords(star, 1000)
        self.move(*self.coords)
        self.show()

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        # self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.draw_stars()

    def draw_stars(self):
        logic_stars = StarsGetter.get_stars()
        # print([s for s in logic_stars])
        # qtstars = [s for s in logic_stars]
        # qtstars = [ QtStar(s) for s in logic_stars ]
        qts = QtStar(logic_stars.__next__(), self)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            # self._zoom = 0

    def setPhoto(self, pixmap=None):
        # print(self._zoom)
        # self._zoom = 0        
        if pixmap and not pixmap.isNull():
            # print('!! set photo')
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            print('was none')
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        # self.fitInView()
        if self._zoom == 0:
            self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            print(self._zoom)
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(QtCore.QPoint(event.pos()))
        super(PhotoViewer, self).mousePressEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.create_widgets()
        self.setLayout(self.get_layout())
        # self.change_view()
        # print(self.viewer.picture)


    def change_view(self):
        ra = self.get_ra_full_sec()
        dec = self.get_dec_full_sec()
        if ra is None or dec is None:
            QtWidgets.QMessageBox.about(self, '', "Wrong input format")
            return
        pic_name = '{}ra_{}dec.png'.format(ra, dec)
        path = os.getcwd()+'/shifts/'+pic_name
        # print(path)
        if not os.path.exists(path):
            print('creating')
            PictureCreator.create_lv(path, (ra, dec))
        # print('going to set photo')
        pixmap = QtGui.QPixmap(path)
        self.pic.setPhoto(pixmap)
        # print('got pixmap')

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

        ra = self.get_ra_full_sec()
        dec = self.get_dec_full_sec()
        if ra is None or dec is None:
            QtWidgets.QMessageBox.about(self, '', "Wrong input format")
            return
        ra += delta[0]
        dec += delta[1]
        self.coords_edit_ra.setText('{} hours {} minutes {} seconds'.format(*self.get_ra_sep_measure(ra)))
        self.coords_edit_dec.setText('{} degrees {} minutes {} seconds'.format(*self.get_dec_sep_measure(dec)))
        self.change_view()

    def get_ra_full_sec(self):
        text = self.coords_edit_ra.text()
        match = re.match(r'(\d+) hours (\d+) minutes (\d+) seconds', text)
        if match is None:
            return None
        h = int(match.group(1))
        m = int(match.group(2))
        s = int(match.group(3))
        # if h >= 24 or m >= 60 or s >= 60:
        #     return None
        return h * 3600 + m * 60 + s

    def get_dec_full_sec(self):
        text = self.coords_edit_dec.text()
        match = re.match(r'(-* *\d+) degrees (\d+) minutes (\d+) seconds', text)
        if match is None:
            return None
        d = int(match.group(1))
        m = int(match.group(2))
        s = int(match.group(3))
        # if d >= 90 or d <= -90 or m >= 60 or s >= 60:
        #     return None
        return -d * 60 * 60 + m * 60 + s

    def get_ra_sep_measure(self, full_sec):
        full_sec = full_sec % (24 * 60 * 60)
        s = full_sec % 60
        h = full_sec // 3600
        m = (full_sec % 3600) // 60
        return (h, m, s)

    def get_dec_sep_measure(self, full_sec):
        # if full_sec > 90 * 3600 or full_sec < -90 * 3600:
            # return None
        if full_sec > 90 * 3600:
            print('>90')
            delta = full_sec - 90 * 3600
            full_sec = - 90 * 3600 + delta
        elif full_sec < -90 * 3600:
            print('<90')
            delta = - 90 * 3600 - full_sec
            full_sec = 90 * 3600 - delta
        s = full_sec % 60
        d = full_sec // 3600
        m = (full_sec % 3600) // 60
        return (-d, m, s)

    def create_widgets(self):
        self.btn_left = QtWidgets.QToolButton()
        self.btn_left.setText('ᐊ')
        self.btn_left.clicked.connect(lambda: self.turn('left'))

        self.btn_right = QtWidgets.QToolButton()
        self.btn_right.setText('ᐅ')
        self.btn_right.clicked.connect(lambda: self.turn('right'))

        self.btn_up = QtWidgets.QToolButton()
        self.btn_up.setText('ᐃ')
        self.btn_up.clicked.connect(lambda: self.turn('up'))

        self.btn_down = QtWidgets.QToolButton()
        self.btn_down.setText('ᐁ')
        self.btn_down.clicked.connect(lambda: self.turn('down'))

        self.coords_edit_ra = QtWidgets.QLineEdit()
        self.coords_edit_ra.setText('0 hours 0 minutes 0 seconds')
        self.coords_edit_dec = QtWidgets.QLineEdit()
        self.coords_edit_dec.setText('0 degrees 0 minutes 0 seconds')

        self.btn_getview = QtWidgets.QToolButton()
        self.btn_getview.setText('Show')
        self.btn_getview.clicked.connect(self.change_view)

        self.pic = PhotoViewer(self)

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
        hbox2.addWidget(self.coords_edit_ra)
        hbox2.addWidget(self.coords_edit_dec)
        hbox2.addWidget(self.btn_getview)
        hbox2.addSpacing(85)
        hbox2.addWidget(self.btn_down)
        hbox2.addSpacing(35)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch()
        vbox.addSpacing(-900)
        vbox.addWidget(self.pic)
        # vbox.addWidget(self.pic2)
        # vbox.addSpacing(80)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox2)
        return vbox


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # window.setGeometry(500, 300, 800, 600)
    window.setGeometry(50, 50, 1800, 800)
    window.show()
    sys.exit(app.exec_())