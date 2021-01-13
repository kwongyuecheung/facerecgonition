from tkinter import *
import tkinter as tk
import cv2
import fnmatch
def getPicture(entry1,entry2):
    name = (entry1.get())
    password = (entry2.get())
    
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera

    cv2.namedWindow("test")
    
    print("空白ボタン押すと写真撮ります。")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
            
        if k%256 == 32:
            # SPACE pressed
            img_name = "images/"+str(name)+".jpg"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            break
        

    cam.release()

    cv2.destroyAllWindows()
