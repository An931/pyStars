import pygame
from pygame.locals import *
from math import sin, cos
from OpenGL.GL import *
from OpenGL.GLU import *
 
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

SIZE = 800
 
class QtStar():
    def __init__(self, star, constellation, parent=None):
        self.star = star
        self.constellation = constellation

        ra_ang = 360 / (24*60*60) * self.star.ra.full_sec
        dec_ang = 360 / (90*60*60) * self.star.dec.full_sec
        self.angles = (ra_ang, dec_ang)



class QtConstellation:
    def __init__(self, text, name, qtstars_parent):
        self.name = name
        lines = text.splitlines()
        self.stars = []
        for l in lines:
            star = Star(l)
            self.stars.append(QtStar(star, self, qtstars_parent))

    def get_constellations(qtstars_parent=None):
        path = './data/'
        txt_files = [x for x in os.listdir(path) if x.endswith('.txt')]


        # stars = []
        for name in txt_files:
            with open(path + name) as f:
                constellation = QtConstellation(f.read(), name[:-4], qtstars_parent)
                yield constellation

def get_stars_points():
    constellations = QtConstellation.get_constellations()
    stars = []
    for c in constellations:
        for s in c.stars:
            stars.append(s)

    angles = []
    for s in stars:
        angles.append(s.angles)
    print(angles)

    points = []
    for a in angles:
        phi = a[0]
        tet = a[1]
        points.append((sin(tet)*cos(phi), sin(tet)*sin(phi), cos(tet)))

    print()
    return points



def Cube():
    glBegin(GL_LINE_LOOP)
    # for edge in edges:
    stars = get_stars_points()


    glEnd()
 
 
def main():
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
 
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
 
    glTranslatef(0.0,0.0, -5)
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
        glRotatef(1, 2, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)
 
 
main()