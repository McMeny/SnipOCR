import cv2
from tkinter import *
from PIL import ImageGrab
import numpy as np
import pytesseract
import pyperclip as pc
import pyautogui
from tkinter import messagebox
from tkinter import filedialog as fd
import time
from tkinter import IntVar
import os
from selenium import webdriver
from pathlib import Path


def findfile(name, path):
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)
global filepath
filepath = findfile('tesseract.exe', '/')
pytesseract.pytesseract.tesseract_cmd = filepath

#-----------------------------------------------------------------------------
def Snip_tool():
    time.sleep(0.13)

    bk_screenshot = pyautogui.screenshot()
    bk_array = np.array(bk_screenshot)
    bk_img = cv2.cvtColor(bk_array, cv2.COLOR_BGR2RGB)

    cv2.namedWindow('background', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("background", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('background', bk_img)

    global n, coords
    n=0
    root = Tk()
    screen_width, screen_height  = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}')
    root.attributes("-alpha", 0.5)
    root.overrideredirect(True)
    canvas = Canvas(root, width = screen_width, height = screen_height)
    canvas.pack()

    x1=y1=coords=None

    def key_release(e):
        root.destroy()

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
        if coords:
            root.withdraw()


        imggrab = ImageGrab.grab(bbox= (coords[0],coords[1],x1, y1))
        img_array = np.array(imggrab)
        img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        cv2.destroyAllWindows()

        win = cv2.namedWindow('Capture')
        cv2.imshow('Capture', img)
        x1=y1=coords=None
        
        if filepath:
            pass
        else:
            messagebox.showerror('tesseract.exe file is not found.', 'The tesseract.exe file has not been found, please go to https://mcmeny.itch.io/snipocr and install the zip folder again.')

        text = pytesseract.image_to_string(img)
        pc.copy(text)
        def text_search(txt):
            def findfile(name, path):
                for dirpath, dirname, filename in os.walk(path):
                    if name in filename:
                        return os.path.join(dirpath, name)
            f = findfile('chromedriver.exe', '/')
            p = Path(f)
            print(p)
            os.environ["PATH"] = f'{os.getenv(os.path)};chromedriver.exe'
            search = txt.replace(' ', '+')
            browser = webdriver.Chrome('chromedriver.exe')
            elements = [browser.get(f'https://www.google.com/searc h?q=' + {search} + str(i)) for i in range(1)]
        text_search(text)
        if text:
            confirmed = messagebox.askyesnocancel('Notification', 'Text successfully copied to clipboard. Would you like to save the image?')
            if confirmed:
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
        text = pytesseract.image_to_string(fle)
        if text:
            messagebox.showinfo('Notification', 'Text successfully copied to clipboard.')
            pc.copy(text)
        else:
            messagebox.showerror('Error', 'This document has unreadable text. Please try again.')
#-----------------------------------------------------------------------------
