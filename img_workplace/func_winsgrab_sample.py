import func_winsgrab as fs
import win32gui
import cv2

hwnd = win32gui.FindWindow(None, r'face - Google Search - Google Chrome')
dimensions = fs.find_windows_dimension_from_hwnd(hwnd)

while (True):
	predictions = fs.predict_screen_from_dimension(dimensions, isShowFps = False)
	#you can get the type of emotion from true_list_of_emotion. true_list_of_emotion[0] = predictions[0]
	print (predictions)

	if cv2.waitKey(25) & 0xFF == ord("q"):
	    cv2.destroyAllWindows()
	    break