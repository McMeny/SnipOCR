from pynput import keyboard
from engine import setn, Snip_tool
from tkinter import filedialog as fd
import cv2

img = 1
COMBINATIONS = [
        {keyboard.Key.shift, keyboard.KeyCode(char='S')}
        ]

current = set()

def execute():
    file_name = fd.asksaveasfilename(filetypes = [('png files', '.png'), ('jpg files', '.jpg')], defaultextension = '.png')
    if file_name:
        cv2.imwrite(file_name, img)

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()