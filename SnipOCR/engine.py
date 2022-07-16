import cv2
from tkinter import *
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PIL import ImageGrab

class Snip_tool(QtWidgets.QWidget):
    isSnipping = False
    background = True
    def __init__(self):
        super(Snip_tool, self).__init__()

        root = Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def start(self):
        Snip_tool.isSnipping = True
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.4)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            print('Quit')
            self.close
        event.accept()

        if Snip_tool.isSnipping:
            def paintEvent(self, event):
                qp = QtGui.QPainter(self)
                qp.setPen(QtGui.QPen(QtGui.QColor('red'), 2))
                qp.setBrush(QtGui.QColor(126, 126, 200, 0))
                qp.drawRect(QtCore.QRect(self.begin, self.end))
        else:
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            qp.setBrush(QtGui.QColor(0, 0, 0, 0))
            self.setWindowOpacity(0)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox = (x1, y1, x2, y2))
        img_array = np.array(img)
        img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        cv2.imshow('Captured', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Snip_tool()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
