import cv2
import numpy as np
import time
import PoseModule as pm
import requests
import pygame  # Import pygame for sound handling

cap = cv2.VideoCapture(0)

detector = pm.PoseDetector()
count = 0
dir = 0
pTime = 0

# Initialize pygame mixer for playing sound
pygame.mixer.init()
song = pygame.mixer.Sound("sound.mp3")  

url = "http://localhost:3000/api/countinc"

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        angle = detector.findAngle(img, 12, 14, 16)
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))

        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
                data = {"count": count}
                response = requests.post(url, json=data)
                print(response.status_code, response.text)

                # Play the song when a push-up is completed
                if  count % 1 == 0:  
                    song.play() 
                    print("Push-up completed! Song is playing!")

        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
                data = {"count": count}
                response = requests.post(url, json=data)
                print(response.status_code, response.text)
                if  count % 1 == 0:  # Play once for every complete push-up
                    song.play()  
                    print("Push-up completed! Song is playing!")
        print(count)

        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", img)
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):  # Press 'q' to quit
        break

