from tkinter import *
from SnipOCR import Snip, Snip_copytool, scan_upload, scan_to_search
from PIL import ImageGrab, Image, ImageTk
import tkinter.font as font
from tkinter import filedialog
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QIcon
from os.path import basename
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen

def main():
    root = Tk()
    w = IntVar()
    w.set(0)
    photo = PhotoImage(file = 'snipocrlogo.png')
    root.iconphoto(False, photo)
    root.title('SnipOCR')
    root.geometry('400x55')
    canvas = Canvas(root, width = 451, height = 238, highlightthickness = 0)
    canvas.grid(columnspan = 100, rowspan = 100)
    root.resizable(False, False)

    fcolor = '#666666'
    bcolor = '#ffffff'

    Snip()
    
    snip_btn = Button(root, width = 10, height = 2, text = 'Snip', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
    fg = bcolor,
    bg = fcolor,
    border = 0,
    activeforeground = fcolor,
    activebackground = bcolor,
    command = Snip())

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

    snip_copy_btn = Button(root, width = 15, height = 2, text = 'Snip & Copy Text', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
    fg = bcolor,
    bg = fcolor,
    border = 0,
    activeforeground = fcolor,
    activebackground = bcolor,
    command = Snip_copytool)

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

    scan_btn = Button(root, width = 20, height = 2, text = 'Convert image to text', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
    fg = bcolor,
    bg = fcolor,
    border = 0,
    activeforeground = fcolor,
    activebackground = bcolor,
    command = scan_upload)

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

    scan_to_search_btn = Button(root, width = 13, height = 2, text = 'Snip and search', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
    fg = bcolor,
    bg = fcolor,
    border = 0,
    activeforeground = fcolor,
    activebackground = bcolor,
    command = scan_to_search)

    def scan_search_button():
        def on_enter(e):
            scan_to_search_btn['background'] = bcolor
            scan_to_search_btn['foreground'] = fcolor

        def on_leave(e):
            if w.get() == 0:
                scan_to_search_btn['background'] = fcolor
                scan_to_search_btn['foreground'] = bcolor
            if w.get() == 1:
                scan_to_search_btn['background'] = 'ededed'
                scan_to_search_btn['foreground'] = '#303030'

        scan_to_search_btn.bind('<Enter>', on_enter)
        scan_to_search_btn.bind('<Leave>', on_leave)

        scan_to_search_btn.place(x = 310, y = 10)

    scan_search_button()

if __name__ == '__main__':
    main()

mainloop()
