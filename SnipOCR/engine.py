import cv2
from tkinter import *
from PIL import ImageGrab
from cv2 import destroyAllWindows
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\minua\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
import pyperclip as pc
import pyautogui
from tkinter import messagebox
from tkinter import filedialog as fd
import time
from tkinter import ttk
import tkinter.font as font

def Settings():
    settings = Tk()
    settings.title('Settings')
    settings.geometry('250x310')
    settings.resizable(False, False)

    text = Label(settings, text = 'Enhance your experience.', font = font.Font(family = 'Sans Serif', size = 10), borderwidth = 0)
    text.pack(side = 'top', pady = 8)

    frame = LabelFrame(settings, text = 'Application')
    frame.pack(side = 'bottom', fill = 'both', expand = 'yes', pady = 3, padx = 3)
    
    cb_value = IntVar()
    cb_value.set(0)
    
    overlay = ttk.Checkbutton(frame, text = 'Turn on screen overlay while snipping?')
    overlay.pack(anchor = 'n')

    #def cb_check():
    #    global overlay_scrn
    #    if cb_value == 1:
    #        overlay_scrn = root.attributes("-alpha", 0.5)
    #    if cb_value == 0:
    #        print(0)

    delay_text = Label(frame, text = 'What would you like to set your delay to?')
    delay_text.place(anchor = 'n', x = 115, y = 30)

    delay = ttk.Combobox(frame, values = ['0 seconds', '1 second', '2 seconds', '5 seconds', '10 seconds'], state = 'readonly')
    delay.set('No delay')

    #def time_delay(event):
    #    global time_delay_value
    #    time_delay_val = delay.get()
    #    time_val = time_delay_val.split()
    #    time_delay_value = time_val[0]
    #    time_delay_value = int(time_delay_value)
    #    print(time_delay_value)

    #delay.bind('<<ComboboxSelected>>', time_delay)

    delay.place(anchor = 'n', x = 80, y = 52)
#-----------------------------------------------------------------------------
def Snip_tool():
    time.sleep(0.13)
    #time.sleep(time_delay_value)

    bk_screenshot = pyautogui.screenshot()
    bk_array = np.array(bk_screenshot)
    bk_img = cv2.cvtColor(bk_array, cv2.COLOR_BGR2RGB)

    win = cv2.namedWindow('background', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("background", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('background', bk_img)

    root = Tk()
    global n, coords, overlay_scrn
    n=0
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}')
    overlay_scrn = root.attributes("-alpha", 0.5)
    root.overrideredirect(True)
    canvas = Canvas(root, width = screen_width, height = screen_height)
    canvas.pack()

    x1=y1=coords=None

    def key_press(e):
        root.destroy()
    def key_release(e):
        root.destroy()

    root.bind('<Key>', key_press)
    root.bind('<KeyRelease>', key_release)

    def cur_press_event(event):
        global n,coords,a
        if n==0:
            n+=1
            coords=event.x,event.y
        elif n==1:
            n+=1
            a=canvas.create_rectangle(coords[0],coords[1],event.x,event.y, fill = 'purple')
        else:
            canvas.coords(a, coords[0] ,coords[1], event.x, event.y)

    def setn(event):
        global n,x1,y1,coords
        n=0
        x1,y1 = event.x, event.y
        if coords is not None:
            root.withdraw()

        imggrab = ImageGrab.grab(bbox= (coords[0],coords[1],x1, y1))
        img_array = np.array(imggrab)
        img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        cv2.destroyAllWindows()

        win = cv2.namedWindow('Capture')
        cv2.imshow('Capture', img)
        x1=y1=coords=None

        text = pytesseract.image_to_string(img)
        pc.copy(text)

        if text:
            question = messagebox.askyesnocancel('Notification', 'Text successfully copied to clipboard. Would you like to save the image?')
            if question:
                file_name = fd.asksaveasfilename(filetypes = [('png files', '.png'), ('jpg files', '.jpg')], defaultextension = '.png')
                if file_name: #file_name could be None!
                    cv2.imwrite(file_name, img)
        else:
            messagebox.showerror('Error', 'The application was not able to copy the text to clipboard. Please try again.')

    root.bind('<B1-Motion>', cur_press_event)
    root.bind('<ButtonRelease-1>',setn)
#-----------------------------------------------------------------------------
def Scan_upload():
    fle = fd.askopenfilename(filetypes = [
        ('text files', '*.txt'),
        ('HTML Files', '*html'),
        ('Python files', '*,py'),
        ('PDF files', '*,pdf'),
        ('All files', '*.*')
        ])

    if fle:
        question = messagebox.showinfo('Notification', 'Text successfully copied to clipboard.')
        text = pytesseract.image_to_string(fle)
        pc.copy(text)
        #messagebox.showerror('Error', 'This document has unreadable text. Please try again.')
#-----------------------------------------------------------------------------
    #def paint_event(event):
    #    global p,paint_coords
    #    if p == 0:
    #        p += 1
    #        paint_coords=event.x,event.y
    #        color = (0, 255, 0)
    #    else:
    #        canvas.coords(paint_coords[0] ,paint_coords[1], event.x, event.y)

    #def setp(event):
    #    global p,x1,y1,paint_coords
    #    p = 0
    #    x1,y1 = event.x, event.y
    #    if paint_coords is not None:
    #        print(*paint_coords)
    #        print(x1, y1)

    #x1=y1=paint_coords=None

    #root.bind('<B1-Motion>', paint_event)
    #root.bind('<ButtonRelease-1>', setp)