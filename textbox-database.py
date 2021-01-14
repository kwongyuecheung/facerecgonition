from tkinter import *
import tkinter as tk

import cv2
import fnmatch
import psycopg2
import Security_key
import face1
#declare final id
final_id = ''
#build the chat box
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
def getName():
    
    final_id = face1.face_function()
    print(final_id)
    namelabel = Label(root, text = final_id)
    canvas1.create_window(120, 210, window=namelabel)
    
    

#open facedetection    
button1 = tk.Button(text='顔認証', command= getName,bg='brown', fg='white')
canvas1.create_window(200, 180, window=button1)

def saveinfo():    
    root2 = tk.Tk()
    def getPicture1():
        #connecting to database
        # 把 Heroku Postgres 的相關資訊寫到下列指令 (database, user, password, host, port)
        conn=psycopg2.connect(database="d4u27skfpv14ni",user="mfvqhpuznumsaa",
        password= "9806c470ce543836af4329fa597e2d403a52d59d686bc10060918093809a1934",
        host="ec2-52-44-46-66.compute-1.amazonaws.com",
        port="5432")
        print("Connection established")

        ##################################################################################

        cursor=conn.cursor()#cursor for database
        #database table info already exsist
        name = entry1.get()
        password = entry2.get()
        #cam = cv2.VideoCapture(0)
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cv2.namedWindow("image_capture")
        print('Press space to take image')
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("image_capture", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "images/"+str(name)+".jpg"
                cv2.imwrite(img_name, frame)
                encrypt_pass = Security_key.encrypt(password)
                cursor.execute("INSERT INTO info (name, password) VALUES (%s, %s);", (name, encrypt_pass))
                print("IMAGE, USER, PASSWORD are saved")
                print("{} written!".format(img_name))
                break
        conn.commit()
        cursor.close()  
        print("Connection closed")  
        #Stop control of camera
        cam.release()
        cv2.destroyAllWindows()
        #close the input window
        root2.destroy()

    canvas1 = tk.Canvas(root2, width = 400, height = 300,  relief = 'raised')
    canvas1.pack()
    root2.title("登録")
    entry1 = tk.Entry (root2)
    canvas1.create_window(210, 230, window=entry1)
    entry2 = tk.Entry (root2,show ='*',width = 20)
    canvas1.create_window(210, 250, window=entry2)

    button3 = tk.Button(root2,text='Get the picture', command = getPicture1)
    canvas1.create_window(200, 180, window=button3)
    root2.mainloop()


#new user
button2 = tk.Button(text='登録', command= saveinfo ,bg='brown', fg='white')
canvas1.create_window(380, 20, window=button2)
root.mainloop()
