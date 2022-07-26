from tkinter import *
import tkinter.font as font
from engine import Snip_tool, Scan_upload
from tkinter import PhotoImage

root = Tk()
root.title('SnipOCR')
root.geometry('198x60')
root.resizable(False, False)

#variables
fcolor = '#666666'
bcolor = '#ffffff'
w = IntVar()
w.set(0)
a = IntVar()
a.set(0)

bottom_text = Label(text = 'Blou, 2022', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0)
bottom_text.pack(anchor = 'sw', side = 'left', padx = 5)

snip_btn = Button(root, width = 12, height = 2, text = 'Image to text', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
    fg = bcolor,
    bg = fcolor,
    border = 0,
    activeforeground = fcolor,
    activebackground = bcolor,
    command = Snip_tool)

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

fileupload_btn = Button(root, width = 13, height = 2, text = 'scan file to text', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
    fg = bcolor,
    bg = fcolor,
    border = 0,
    activeforeground = fcolor,
    activebackground = bcolor,
    command = Scan_upload)

def file_uploadbutton():
    def on_enter(e):
        fileupload_btn['background'] = bcolor
        fileupload_btn['foreground'] = fcolor

    def on_leave(e):
        if a.get() == 0:
            fileupload_btn['background'] = fcolor
            fileupload_btn['foreground'] = bcolor
        if a.get() == 1:
            fileupload_btn['background'] = 'ededed'
            fileupload_btn['foreground'] = '#303030'

    fileupload_btn.bind('<Enter>', on_enter)
    fileupload_btn.bind('<Leave>', on_leave)

fileupload_btn.place(x = 100, y = 10)

file_uploadbutton()

mainloop()