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

root = Tk()
root.title('Snip OCR tool')
root.geometry('400x55')
canvas = Canvas(root, width = 451, height = 238, highlightthickness = 0)
canvas.grid(columnspan = 100, rowspan = 100)
root.resizable(False, False)

#variables
w = IntVar()
w.set(0)
fcolor = '#666666'
bcolor = '#ffffff'

def snip_mech():
    from PyQt5 import QtCore, QtGui, QtWidgets
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

            cv2.imshow('Captured', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = Snip_copytool()
        window.show()
        app.aboutToQuit.connect(app.deleteLater)
        sys.exit(app.exec_())

def snip():
    snip_mech()

snip_btn = Button(root, width = 10, height = 2, text = 'Snip', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
fg = bcolor,
bg = fcolor,
border = 0,
activeforeground = fcolor,
activebackground = bcolor,
command = snip)


def snipbutton():
    def on_enter(e):
        snip_btn['background'] = bcolor
        snip_btn['foreground'] = fcolor

    def on_leave(e):
        if w.get() == 0:
            snip_btn['background'] = fcolor
            snip_btn['foreground'] = bcolor
        if w.get() == 1:
            snip_btn['background'] = 'ededed'
            snip_btn['foreground'] = '#303030'

    snip_btn.bind('<Enter>', on_enter)
    snip_btn.bind('<Leave>', on_leave)

    snip_btn.place(x = 10, y = 10)

snipbutton()

def snip_copy():
    from PyQt5 import QtCore, QtGui, QtWidgets
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

            cv2.imshow('Captured', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = Snip_copytool()
        window.show()
        app.aboutToQuit.connect(app.deleteLater)
        sys.exit(app.exec_())

snip_copy_btn = Button(root, width = 15, height = 2, text = 'Snip & Copy Text', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
fg = bcolor,
bg = fcolor,
border = 0,
activeforeground = fcolor,
activebackground = bcolor,
command = snip_copy)

def snip_copy_button():
    def on_enter(e):
        snip_copy_btn['background'] = bcolor
        snip_copy_btn['foreground'] = fcolor

    def on_leave(e):
        if w.get() == 0:
            snip_copy_btn['background'] = fcolor
            snip_copy_btn['foreground'] = bcolor
        if w.get() == 1:
            snip_copy_btn['background'] = 'ededed'
            snip_copy_btn['foreground'] = '#303030'

    snip_copy_btn.bind('<Enter>', on_enter)
    snip_copy_btn.bind('<Leave>', on_leave)

    snip_copy_btn.place(x = 80, y = 10)

snip_copy_button()

def scan():
    fle = filedialog.askopenfilename(initialdir = 'C:/gui/', title = 'Open File', filetypes = (('text files', '*.txt'), ('HTML Files', '*html'), ('Python files', '*,py'), ('All files', '*.*')))
    text = pytesseract.image_to_string(fle)
    print(text)
    pc.copy(text)

    pop_up = Toplevel(root)
    pop_up.geometry('200x60')
    pop_up.title('Notification')
    popup_label = Label(pop_up, text = 'Text copied to clipboard!', font = font.Font(family = 'MS Shell Dlg 2', size = 8))
    popup_label.place(x = 40, y = 10)
    ok_btn = Button(pop_up, text = 'Ok', command = pop_up.destroy)
    ok_btn.place(x = 80, y = 30)

scan_btn = Button(root, width = 20, height = 2, text = 'Convert image to text', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
fg = bcolor,
bg = fcolor,
border = 0,
activeforeground = fcolor,
activebackground = bcolor,
command = scan)

def scan_button():
    def on_enter(e):
        scan_btn['background'] = bcolor
        scan_btn['foreground'] = fcolor

    def on_leave(e):
        if w.get() == 0:
            scan_btn['background'] = fcolor
            scan_btn['foreground'] = bcolor
        if w.get() == 1:
            scan_btn['background'] = 'ededed'
            scan_btn['foreground'] = '#303030'

    scan_btn.bind('<Enter>', on_enter)
    scan_btn.bind('<Leave>', on_leave)

    scan_btn.place(x = 180, y = 10)

scan_button()

#construction of the settings window

def settings():
    print('settings')
    class Settings(QWidget):
        def __init__(self):
            super().__init__()
    app = QApplication(sys.argv)

    window = Settings()
    window.resize(400,400)
    window.show()


    sys.exit(app.exec())



settings_btn = Button(root, width = 10, height = 2, text = 'Settings', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
fg = bcolor,
bg = fcolor,
border = 0,
activeforeground = fcolor,
activebackground = bcolor,
command = settings)

def settings_button():
    def on_enter(e):
        settings_btn['background'] = bcolor
        settings_btn['foreground'] = fcolor

    def on_leave(e):
        if w.get() == 0:
            settings_btn['background'] = fcolor
            settings_btn['foreground'] = bcolor
        if w.get() == 1:
            settings_btn['background'] = 'ededed'
            settings_btn['foreground'] = '#303030'

    settings_btn.bind('<Enter>', on_enter)
    settings_btn.bind('<Leave>', on_leave)

    settings_btn.place(x = 310, y = 10)

settings_button()

mainloop()
