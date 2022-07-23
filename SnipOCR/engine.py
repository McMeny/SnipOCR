from logging import root
import cv2
from tkinter import *
from PIL import ImageGrab, Image, ImageTk
import sys
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\minua\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
import struct
import array

def Snip_tool():
    root = Tk()
    global n, coords
    n=0
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}')
    root.attributes("-alpha", 0.5)
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
#-----------------------------------------------------------------------------
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
            
            
        def photo_image(image: np.ndarray):
            height, width = img_array.shape[:2]
            header = f'P6 {width} {height} 255'.encode()
            img_data = header + cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR).tobytes()
            img_struct = struct.unpack('f', img_data)
            return PhotoImage(width = width, height = height, data = img_struct, format = 'PPM')

            
        imggrab = ImageGrab.grab(bbox= (coords[0],coords[1],x1, y1))
        img_array = np.array(imggrab)
        img_shape = img_array.shape[:2]
        img = photo_image(img_array)

        img_canvas = Canvas(root, width = 300, height = 300)
        img_canvas.pack()
        img_canvas.create_image(img_shape[0], img_shape[1], anchor = 'nw', image = img)

            #win = cv2.namedWindow('Snip Window')
            #cv2.imshow('Snip Window', image)
        x1=y1=coords=None

    root.bind('<B1-Motion>', cur_press_event)
    root.bind('<ButtonRelease-1>',setn)
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