import sys
# this is where python stores modules, yours could be different
sys.path.append(
    r"C:\Users\MIMS-PC\AppData\Local\Programs\Python\Python39\Lib\site-packages")
sys.path.append(r"E:\school_teams\environment2\Lib\site-packages")

import time
import traceback
import cv2
import imagezmq
import numpy as np
import simplejpeg
from imutils.video import FPS


firstRecv = True
prevRecv = 0
latency = 0

cameraFPS = 60

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 50)
fontScale = 2
fontColor = (155, 0, 0)
thickness = 1
lineType = 2

# try:
# with imagezmq.ImageHub() as image_hub:

image_hub = imagezmq.ImageHub(open_port='tcp://192.168.2.61:8000')

while True:                    # receive images until Ctrl-C is pressed
    sent_from, image = image_hub.recv_jpg()
    image = simplejpeg.decode_jpeg(image, colorspace='BGR') # 'BGR' space is the default colour space by opencv , uncompresses the compressed jpg file sent from the rpi 

    if firstRecv:
        firstRecv = False
        prevRecv = round(time.time() * 1000)
    else:
        latency = (round(time.time() * 1000) - prevRecv) / 2 - round((1/cameraFPS * 1000) / 2)
        prevRecv = round(time.time() * 1000)
        cv2.putText(image, 'Ping: ' + str(latency), bottomLeftCornerOfText, font,fontScale, fontColor, thickness, lineType)  # Adds the ping count to the image

    # display images 1 window per sent_from
    cv2.imshow(sent_from, image)
    image_hub.send_reply(b'OK')   # sends bytes 'OK' to let the sender know that data was received  

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()         # closes the windows opened by cv2.imshow()
sys.exit()
