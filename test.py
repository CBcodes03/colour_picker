import cv2
import numpy as np
import pyautogui
import tkinter as tk
from pynput import mouse, keyboard
import sys

pallete=[]
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.withdraw()

def get_color_from_screen(x, y):
    global pallete
    screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
    color_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)[0, 0]
    color_rgb = color_bgr[::-1]
    hex_color = '#{:02X}{:02X}{:02X}'.format(color_rgb[0], color_rgb[1], color_rgb[2])
    pallete.append(hex_color)
    return color_rgb, hex_color

def on_press(key, mouse_listener):
    try:
        if key.page_down:
            mouse_listener.stop()
            pyautogui.alert(text=pallete)
            sys.exit()
        elif key.esc:
            main()  # Restart main listener
    except AttributeError:
        pass

def on_click(x, y, button, pressed, mouse_listener):
    if pressed:
        if button == mouse.Button.left:
            color_rgb, hex_color = get_color_from_screen(x, y)
            print(f"RGB: {color_rgb}, Hex: {hex_color}")
        elif button == mouse.Button.right:
            mouse_listener.stop()
            with keyboard.Listener(on_press=lambda key: on_press(key, mouse_listener)) as key_listener:
                key_listener.join()

def main():
    print("Left click anywhere on the screen to get the color, right click to pause, and press 'page_down' to exit page_up to restar")
    with mouse.Listener(on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, mouse.Listener(on_click=on_click))) as listener:
        listener._on_click = lambda x, y, button, pressed: on_click(x, y, button, pressed, listener)
        listener.join()

main()