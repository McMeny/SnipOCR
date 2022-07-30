from tkinter import *
import tkinter.font as font
from engine import Snip_tool, Scan_upload
from tkinter import PhotoImage
import wmi

root = Tk()
root.title('SnipOCR')
root.geometry('240x60')
root.resizable(False, False)

def bg_destroy():
    trm_pcs, name = 0, 'SnipOCR.exe'
    f = wmi.WMI()
    for process in f.Win32_Process():
        if process.name == name:
            process.Terminate()
            trm_pcs += 1
    root.destroy()
root.protocol('WM_DELETE_WINDOW', bg_destroy)

#variables
fcolor, bcolor = '#666666', '#ffffff'
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
            snip_btn['background'], snip_btn['foreground'] = bcolor, fcolor

        def on_leave(e):
            if w.get() == 0:
                snip_btn['background'], snip_btn['foreground'] = fcolor, bcolor
            if w.get() == 1:
                snip_btn['background'], snip_btn['foreground'] = 'ededed', '#303030'

        snip_btn.bind('<Enter>', on_enter)
        snip_btn.bind('<Leave>', on_leave)

        snip_btn.place(x = 30, y = 10)

snipbutton()

fileupload_btn = Button(root, width = 12, height = 2, text = 'file to text', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
    fg = bcolor,
    bg = fcolor,
    border = 0,
    activeforeground = fcolor,
    activebackground = bcolor,
    command = Scan_upload)

def fileuploadbutton():
        def on_enter(e):
            fileupload_btn['background'], fileupload_btn['foreground'] = bcolor, fcolor

        def on_leave(e):
            if w.get() == 0:
                fileupload_btn['background'],fileupload_btn['foreground'] = fcolor, bcolor
            if w.get() == 1:
                fileupload_btn['background'], fileupload_btn['foreground'] = 'ededed', '#303030'

        fileupload_btn.bind('<Enter>', on_enter)
        fileupload_btn.bind('<Leave>', on_leave)
        fileupload_btn.place(x = 130, y = 10)

fileuploadbutton()
mainloop()