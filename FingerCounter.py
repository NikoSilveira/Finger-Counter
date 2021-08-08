import cv2
import time
import os
import HandTrackingModule as htm

#### Parameters ####
cam_width, cam_height = 640, 480

#### Video Capture ####
cap = cv2.VideoCapture(0) #Camera
cap.set(3, cam_width)
cap.set(4, cam_height)

#### Overlay images ####
folder_path = "Hands"
my_list = os.listdir(folder_path)
overlay_list = []

for imPath in my_list:
    image = cv2.imread(f'{folder_path}/{imPath}')
    overlay_list.append(image)


prev_time = 0
detector = htm.handDetector()

while True:
    success, img = cap.read() #Hand image

    #Overlay images
    overlay_list[0] = cv2.resize(overlay_list[0], (200,200)) #resize overlay img
    img[0:200, 0:200] = overlay_list[0]                      #height limit, width limit

    #FPS
    current_time = time.time()
    fps = 1/(current_time - prev_time)
    prev_time = current_time
    cv2.putText(img, 'FPS: '+str(int(fps)), (10,30), cv2.FONT_HERSHEY_PLAIN, 1.5, (255,60,0), 2) #display in window

    cv2.imshow("Finger counter (press Q to exit)", img)
    if cv2.waitKey(1) == ord('q'):
        break