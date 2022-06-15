import cv2
from tkinter import *
from PIL import ImageGrab, Image, ImageTk
import tkinter.font as font
import sys
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\minua\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
import pyperclip as pc
from tkinter import filedialog
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QIcon
from os.path import basename
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen

def Snip():
    class Snip_tool(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            self.setGeometry(0,0, screen_width, screen_height)
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            self.setWindowOpacity(0.4)
            QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
            )
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.show()
            root.withdraw()

        def paintEvent(self, event):
            qp = QtGui.QPainter(self)
            qp.setPen(QtGui.QPen(QtGui.QColor('red'), 2))
            qp.setBrush(QtGui.QColor(126, 126, 200, 0))
            qp.drawRect(QtCore.QRect(self.begin, self.end))

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

#---------------------------------------------------------------
class Snip_copytool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0,0, screen_width, screen_height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.4)
        QtWidgets.QApplication.setOverrideCursor(
        QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()
        root.withdraw()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('red'), 2))
        qp.setBrush(QtGui.QColor(126, 126, 200, 0))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

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

        text = pytesseract.image_to_string(img)
        pc.copy(text)
        print(text)

        if numpy_image is not None and snip_number is not None:
            self.image = self.convert_numpy_img_to_qpixmap(numpy_image)
            self.change_and_set_title("Snip #{0}".format(snip_number))
        else:
            self.image = QPixmap("background.PNG")
            self.change_and_set_title(Menu.default_title)

    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = Snip_copytool()
        window.show()
        app.aboutToQuit.connect(app.deleteLater)
        sys.exit(app.exec_())

#-----------------------------------------------------------------------------------------------
class scan_upload(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        print('testing')
        fle = filedialog.askopenfilename(initialdir = 'C:/gui/', title = 'Open File', filetypes = (('text files', '*.txt'), ('HTML Files', '*html'), ('Python files', '*,py'), ('All files', '*.*')))
        text = pytesseract.image_to_string(fle)
        pc.copy(text)


#-----------------------------------------------------------------------------------------------
class scan_to_search(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        print('scan_to_search')
