import sys
sys.path.append('../')
import time
import numpy as np
import cv2
from PIL import ImageGrab
import win32gui
import win32com.client
from src.fermodelv2 import FERModel
    
#start

cascPath = "./src/haarcascade_frontalface_default.xml"
    
target_emotions = ['anger', 'happiness', 'calm']
true_list_of_emotion = ['anger', 'calm', 'happiness']
model = FERModel(target_emotions, cascPath, verbose=True)

def find_windows_dimension_from_hwnd(hwnd):
    if hwnd == 0:
        print("no window found")
        return []
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)
    dimensions = win32gui.GetWindowRect(hwnd)

    #crop out the top menu bar
    dimensionsST = list(dimensions)
    dimensionsST[1] = dimensionsST[1] + 40

    return dimensionsST


# cut away top bar

isFirst = True
def predict_screen_from_dimension(dimensions, isShowFps = False):
    last_time = time.time()

    image = ImageGrab.grab(dimensions)
    image = image.convert('RGB')
    image = np.array(image)
    image = image.astype(np.uint8)
    predictions = model.predict(image, isFirst)

    #showing fps for debug purposes
    if isShowFps == True:
        print("fps: {0}".format(1 / (time.time() - last_time)))

    return predictions

    
