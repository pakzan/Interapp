import sys
sys.path.append('../')
import time
import numpy as np
import cv2
from PIL import ImageGrab
import win32gui
import win32com.client
from src.fermodelv2 import FERModel
    
cascPath = "./src/haarcascade_frontalface_default.xml"

#start
target_emotions = ['anger', 'happiness', 'calm']
true_list_of_emotion = ['anger', 'calm', 'happiness']
model = FERModel(target_emotions, cascPath, verbose=True)

isFirst = True
while(True):
	last_time = time.time()

	#img here
	if isFirst == True:
		hwnd = win32gui.FindWindow(None, r'face - Google Search - Google Chrome')
		if hwnd == 0:
			print("no window found")
			break
		shell = win32com.client.Dispatch("WScript.Shell")
		shell.SendKeys('%')
		win32gui.SetForegroundWindow(hwnd)
		dimensions = win32gui.GetWindowRect(hwnd)

		# cut away top bar
		dimensionsST = list(dimensions)
		dimensionsST[1] = dimensionsST[1] + 40
	image = ImageGrab.grab(dimensionsST)
	image = image.convert('RGB')
	image = np.array(image)
	image = image.astype(np.uint8)
	predictions = model.predict(image, isFirst)
	if isFirst == True:
		isFirst = False
		print(predictions)
		break

	print("fps: {0}".format(1 / (time.time() - last_time)))
	# Press "q" to quit
	if cv2.waitKey(25) & 0xFF == ord("q"):
	    cv2.destroyAllWindows()
	    break
