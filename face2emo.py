import cv2
import time
import numpy as np
from PIL import ImageGrab
import win32gui
import win32com.client
from src.fermodelv2 import FERModel

import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = None
from constant import DEBUG, EMPTY_FACE_PROB

cascPath = "./src/haarcascade_frontalface_default.xml"
    
target_emotions = ['anger', 'happiness', 'calm']
model = FERModel(target_emotions, cascPath, verbose=True)
debug = DEBUG
destory_debug_window = False

def find_windows_dimension_from_hwnd(hwnd):
    if hwnd == 0:
        print("no window found")
        return []
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)

    dimensions = list(win32gui.GetWindowRect(hwnd))
    # crop out the top menu bar
    dimensions[1] += 40

    return dimensions


def pred_face_from_dimension(dimensions, show_fps = False):
    global destory_debug_window
    last_time = time.time()

    img = ImageGrab.grab(dimensions)
    if img.width * img.height == 0:
        return EMPTY_FACE_PROB

    img = img.convert('RGB')
    img = np.array(img, dtype=np.uint8)
    faces_prob = model.predict(img, debug)
    if destory_debug_window:
        cv2.destroyWindow("captured image")
        destory_debug_window = False

    #showing fps for debug purposes
    if show_fps:
        print("fps: {0}".format(1 / (time.time() - last_time)))

    if not faces_prob:
        return EMPTY_FACE_PROB
    return tuple(np.mean(faces_prob, axis=0))

    
if __name__=="__main__":
    hwnd = win32gui.FindWindow(None, r'face - Google Search - Google Chrome')
    dimensions = find_windows_dimension_from_hwnd(hwnd)

    while (True):
        preds = pred_face_from_dimension(dimensions, show_fps = False)
        #you can get the type of emotion from true_list_of_emotion. true_list_of_emotion[0] = predictions[0]
        print(preds)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break