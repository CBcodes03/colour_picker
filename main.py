import cv2
import sys
import numpy as np
import pyautogui
import tkinter as tk
from pynput import mouse
# Initialize the Tkinter window (only for capturing screen coordinates)
root = tk.Tk()
root.withdraw()  # Hide the main window

# Global variables for storing coordinates
start_x, start_y, end_x, end_y = 0, 0, 0, 0
selecting = False

# Function to calculate the average color of the selected region
def calculate_average_color(region):
    # Calculate the mean of each channel (BGR)
    avg_color = cv2.mean(region)[:3]  # Only take BGR values, ignore alpha
    # Convert BGR to RGB and format as hex
    hex_color = '#{:02X}{:02X}{:02X}'.format(int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))
    return hex_color

# Mouse callback function to select a region
def on_click(x, y, button, pressed):
    global start_x, start_y, end_x, end_y, selecting
    
    if pressed:
        start_x, start_y = x, y
        selecting = True
    else:
        end_x, end_y = x, y
        selecting = False
        # Capture the selected region
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)
        screenshot = pyautogui.screenshot(region=(min(start_x, end_x), min(start_y, end_y), width, height))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        # Display the selected region
        def draw_circle(event,x,y,flags,param):
            if event == cv2.EVENT_RBUTTONDOWN:
                cords=pyautogui.position()
                print(cords)
        # Creating a callback function
        cv2.namedWindow(winname='selected_portion')
        cv2.setMouseCallback('selected_portion',draw_circle)
        while True:
            cv2.imshow('selected_portion',screenshot)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        cv2.destroyAllWindows()
def mf():
    with mouse.Listener(on_click=on_click) as listener:
        print("Click and drag to select a region on the screen.")
        listener.join()

if __name__ == '__main__':
    mf()