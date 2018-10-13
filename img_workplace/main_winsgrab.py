import sys
sys.path.append('../')
import time
import numpy as np
import cv2
from PIL import ImageGrab
import win32gui
from src.fermodelv2 import FERModel
    
cascPath = "./src/haarcascade_frontalface_default.xml"

#start
target_emotions = ['happiness', 'disgust', 'surprise']
model = FERModel(target_emotions, cascPath, verbose=True)

# while(True):
last_time = time.time()

#img here
hwnd = win32gui.FindWindow(None, r'YouTube - Google Chrome')
print (hwnd)
win32gui.SetForegroundWindow(hwnd)
dimensions = win32gui.GetWindowRect(hwnd)

image = ImageGrab.grab(dimensions)
image = image.convert('RGB')
image = np.array(image)
image = image.astype(np.uint8)
model.predict(image)
cv2.imshow("the screen got", image)

print("fps: {0}".format(1 / (time.time() - last_time)))

# Press "q" to quit
if cv2.waitKey(25) & 0xFF == ord("q"):
    cv2.destroyAllWindows()
    # break
    