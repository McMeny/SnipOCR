from tkinter import *
import tkinter.font as font
from engine import Snip_tool, Scan_upload, Settings

root = Tk()
root.title('SnipOCR')
root.geometry('280x60')
root.resizable(False, False)

#variables
fcolor = '#666666'
bcolor = '#ffffff'
w = IntVar()
w.set(0)
a = IntVar()
a.set(0)

bottom_text = Label(text = 'Blou, 2022', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0)
bottom_text.place(x = 100, y = 42)

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

    def on_release_event(e):
        root.withdraw()

    snip_btn.bind('<Enter>', on_enter)
    snip_btn.bind('<Leave>', on_leave)
    snip_btn.bind('<ButtonRelease-1>', on_release_event)

snip_btn.place(x = 10, y = 10)

snipbutton()

fileupload_btn = Button(root, width = 12, height = 2, text = 'scan file to text', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
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

settings_btn = Button(root, width = 12, height = 2, text = 'Settings', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
    fg = bcolor,
    bg = fcolor,
    border = 0,
    activeforeground = fcolor,
    activebackground = bcolor,
    command = Settings)

def settingsbutton():
    def on_enter(e):
        settings_btn['background'] = bcolor
        settings_btn['foreground'] = fcolor

    def on_leave(e):
        if a.get() == 0:
            settings_btn['background'] = fcolor
            settings_btn['foreground'] = bcolor
        if a.get() == 1:
            settings_btn['background'] = 'ededed'
            settings_btn['foreground'] = '#303030'

    settings_btn.bind('<Enter>', on_enter)
    settings_btn.bind('<Leave>', on_leave)

settings_btn.place(x = 190, y = 10)

settingsbutton()

mainloop()