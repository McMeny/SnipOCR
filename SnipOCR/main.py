from tkinter import *
import tkinter.font as font

root = Tk()
root.title('SnipOCR')
root.geometry('400x50')
root.resizable(False, False)

#variables
fcolor = '#666666'
bcolor = '#ffffff'
w = IntVar()
w.set(0)

bottom_text = Label(text = 'Blou, 2022', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0)
bottom_text.place(x = 160, y = 35)

snip_btn = Button(root, width = 10, height = 2, text = 'Snip', font = font.Font(family = 'MS Shell Dlg 2', size = 8), borderwidth = 0,
fg = bcolor,
bg = fcolor,
border = 0,
activeforeground = fcolor,
activebackground = bcolor)

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


mainloop()