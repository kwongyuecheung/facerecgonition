from tkinter import *
import tkinter as tk

import cv2
import fnmatch



root = tk.Tk()
canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
canvas1.pack()
root.title("ようこそ、顔認証システム")
lbl = Label(root, text="顔認証ボタンを押してください")
canvas1.create_window(200, 100, window=lbl)
lbl2 = Label(root, text="パスワード：")
canvas1.create_window(120, 230, window=lbl2)
entry1 = tk.Entry (root) 
canvas1.create_window(210, 230, window=entry1)


#open facedetection    
button1 = tk.Button(text='顔認証', command= lambda:exec(open("face1.py").read()),bg='brown', fg='white')
canvas1.create_window(200, 180, window=button1)

def saveinfo():    
    root = tk.Tk()
    def getPicture1():
        x = entry1.get()
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "images/"+str(x)+".jpg"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
            

        cam.release()

        cv2.destroyAllWindows()

    canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
    canvas1.pack()
    root.title("登録")
    entry1 = tk.Entry (root)
    canvas1.create_window(210, 230, window=entry1)

    button3 = tk.Button(root,text='Get the picture', command = getPicture1)
    canvas1.create_window(200, 180, window=button3)
    root.mainloop()


#new user
button2 = tk.Button(text='登録', command= saveinfo ,bg='brown', fg='white')
canvas1.create_window(380, 20, window=button2)
root.mainloop()
