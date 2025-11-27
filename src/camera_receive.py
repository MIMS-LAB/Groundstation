import sys

sys.path.append(r"D:\alessandro\Thesis\Onboard-Firmware\include\rrc_encoder\src")
sys.path.append(r"C:\Users\RUMIM\AppData\Roaming\Python\Python312\site-packages")

import cv2

# Replace with your ESP32-CAM stream URL
url ="http://192.168.4.1/stream"
# Open the video stream
cap = cv2.VideoCapture(url)
print("meeep")
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()
print("skirtttt")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break
    print("mewow")

    cv2.imshow("ESP32-CAM Stream", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
