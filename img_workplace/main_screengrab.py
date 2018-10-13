import sys
sys.path.append('../')
import time
from src.fermodelv2 import FERModel
import numpy as np
import cv2
    
from mss import mss
mon = {'top': 0, 'left': 0, 'width': 1366, 'height': 768}

sct = mss()

cascPath = "./src/haarcascade_frontalface_default.xml"

#start
target_emotions = ['happiness', 'disgust', 'surprise']
model = FERModel(target_emotions, cascPath, verbose=True)

while(True):
    last_time = time.time()

    # Get raw pixels from the screen, save it to a Numpy array
    img = np.array(sct.grab(mon))

    model.predict(img)

    print("fps: {0}".format(1 / (time.time() - last_time)))

# Press "q" to quit
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break