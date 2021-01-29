from tkinter import *
import tkinter as tk

import cv2
import fnmatch
import psycopg2
import Security_key
import face1
import re
import datetime
from PIL import ImageTk, Image
import os

#build the chat box
root = tk.Tk()
canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
canvas1.pack()
root.title("ようこそ、顔認証システム")
lbl = Label(root, text="顔認証ボタンを押してください")
canvas1.create_window(200, 100, window=lbl)
userlabel = Label(root, text="ユーザーID：")
canvas1.create_window(120, 210, window=userlabel)
lbl2 = Label(root, text="パスワード：")
canvas1.create_window(120, 230, window=lbl2)
entry1 = tk.Entry (root,show ='*') 
canvas1.create_window(210, 230, window=entry1)
def getName():
    global final_id
    final_id = face1.face_function()
    print(final_id)
    #show word in userid input
    namelabel = Label(root, text = final_id)
    canvas1.create_window(180, 210, window=namelabel)
    #show picture
    if (final_id == "認証失敗"):
        filename = '認証失敗.jpg'
    else:
        filename = 'images\\' + final_id + '.jpg'
    img = Image.open(filename)
    resized_img = img.resize((140, 110))
    root.photoimg = ImageTk.PhotoImage(resized_img)
    labelimage = tk.Label(root, image=root.photoimg)
    labelimage.place(x = 130, y = 10)
    
def check_password(): 
    
    #connecting to database
    # 把 Heroku Postgres 的相關資訊寫到下列指令 (database, user, password, host, port)
    conn=psycopg2.connect(database="d4u27skfpv14ni",user="mfvqhpuznumsaa",
    password= "9806c470ce543836af4329fa597e2d403a52d59d686bc10060918093809a1934",
    host="ec2-52-44-46-66.compute-1.amazonaws.com",
    port="5432")
    print("Connection established")
    cursor=conn.cursor()

    #get password from database
    cursor.execute("SELECT password FROM info WHERE name ='" + final_id + "'" )

    result = cursor.fetchone()
    result_word = result[0]
    conn.commit()
    cursor.close()
    print("Connection closed")  
    #print (result_word)
    decrypted_password = Security_key.decrypt(result_word)
    
    #get local password input
    USER_INPUT_PASSWORD = entry1.get()
    #print (USER_INPUT_PASSWORD)
    if(decrypted_password == USER_INPUT_PASSWORD):
        now = datetime.datetime.now()
        condrag = "認証成功\n",now
        
        loginword = Label(root, text = condrag)
        canvas1.create_window(190, 130, window=loginword)

        #Store time on database
        conn=psycopg2.connect(database="dd4a12s1ulg1i7",user="ggtstohzdunlwq",
        password= "53d079c43c336eb6700fae72f30d9511de4753866cce0a079b5a43a22a4e1809",
        host="ec2-34-197-25-109.compute-1.amazonaws.com",
        port="5432")
        print("Connection established")

        cursor=conn.cursor()
        name = final_id
        cursor.execute('insert into time_date(name, time) values(%s, %s)', (name, now))
        print("Time recored")
        conn.commit()
        cursor.close()
        print("Connection closed")  
    else:
        condrag = "----パスワード間違います----\n--------------------------------"
        loginword = Label(root, text = condrag)
        canvas1.create_window(190, 130, window=loginword)
    ##################################################################################

     

#open facedetection    
button1 = tk.Button(text='顔認証', command= getName,bg='brown', fg='white')
canvas1.create_window(170, 180, window=button1)

#check password
check = tk.Button(text='登録', command= check_password,bg='brown', fg='white')
canvas1.create_window(220, 180, window=check)

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
        cv2.namedWindow("PRESS_SPACE_BAR_TO_TAKE_PICTURE")
        print('Press space to take image')
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("PRESS_SPACE_BAR_TO_TAKE_PICTURE", frame)

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
    login = Label(root2, text = "ユーザーID：")
    canvas1.create_window(110, 230, window=login)
    password = Label(root2, text = "パスワード：")
    canvas1.create_window(110, 250, window=password)
    button3 = tk.Button(root2,text='写真撮影', command = getPicture1,bg='brown', fg='white')
    canvas1.create_window(200, 180, window=button3)
    root2.mainloop()


#new user
button2 = tk.Button(text='新規登録', command= saveinfo ,bg='brown', fg='white')
canvas1.create_window(360, 20, window=button2)

root.mainloop()
