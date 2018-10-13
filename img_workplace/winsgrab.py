import numpy as np
import cv2
from PIL import ImageGrab
import win32gui
import win32com.client


#img here
hwnd = win32gui.FindWindow(None, r'YouTube - Google Chrome')
shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')
win32gui.SetForegroundWindow(hwnd)
dimensions = win32gui.GetWindowRect(hwnd)

image = ImageGrab.grab(dimensions)
image = image.convert('RGB')
image = np.array(image)
image = image.astype(np.uint8)
# model.predict(image)
cv2.imshow("the screen got", image)

cv2.waitKey(0)

print ("hello")