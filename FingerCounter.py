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

#### Landmark lists ####
tip_ids = [4, 8, 12, 16, 20]


prev_time = 0
detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read() #Hand image
    img = detector.findHands(img)
    lm_list = detector.findPosition(img)

    #Check fingers
    if len(lm_list) != 0:
        finger_list = []

        #Thumb
        if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0]-1][1]:  #if tip left of nearest phalange
            finger_list.append(1)
        else:
            finger_list.append(0)

        #Other 4 fingers
        for id in range(1,5):                                        #iterate through tips
            if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id]-2][2]:  #if tip above phalange
                finger_list.append(1)
            else:
                finger_list.append(0)

        total_fingers = finger_list.count(1)

        #Overlay images
        overlay_list[total_fingers-1] = cv2.resize(overlay_list[total_fingers-1], (200,200)) #resize overlay img
        img[0:200, 0:200] = overlay_list[total_fingers-1]                                    #height limit, width limit
        
        #Finger count text
        cv2.rectangle(img, (20,280), (130,400), (0,200,0), cv2.FILLED)
        cv2.putText(img, str(total_fingers), (45,375), cv2.FONT_HERSHEY_PLAIN, 6, (255,60,0), 12)

    #FPS
    current_time = time.time()
    fps = 1/(current_time - prev_time)
    prev_time = current_time
    cv2.putText(img, 'FPS: '+str(int(fps)), (10,30), cv2.FONT_HERSHEY_PLAIN, 1.5, (255,60,0), 2) #display in window

    cv2.imshow("Finger counter (press Q to exit)", img)
    if cv2.waitKey(1) == ord('q'):
        break