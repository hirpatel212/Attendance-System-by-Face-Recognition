from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector 
from time import strftime
from datetime import datetime
import cv2
import os
import numpy as np

class Face_Recognition:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        #Title
        title_lbl = Label(self.root, text=" FACE RECOGNITION ",font=("times new roman", 35, "bold"), bg="white", fg="sienna")
        title_lbl.place(x=0, y=0,width=1530,height=45)

        #Image 1
        img_top1 = Image.open("images/facerecignition1.png").resize((700, 750), Image.LANCZOS)
        self.photoimg_top1 = ImageTk.PhotoImage(img_top1)
        f_lbl2 = Label(self.root, image=self.photoimg_top1)
        f_lbl2.place(x=5, y=55, width=700, height=750)

        #Image 2
        img_bottom = Image.open("images/facerecognition2.png").resize((950, 750), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        f_lbl3 = Label(self.root, image=self.photoimg_bottom)
        f_lbl3.place(x=700, y=55, width=950, height=750)

        #Button 
        bt1_1 = Button(f_lbl3 , text="Face Recognition", cursor="hand2",command=self.face_recog, font=("times new roman",20, "bold"), bg="gold", fg="black")
        bt1_1.place(x=380, y=680, width=200, height=40)

    # ============= attendance =======================
    
    def mark_attendance(self,i,r,n,d):
        with open("hmv.csv","r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = []
            for line in myDataList:
                entry = line.split((","))
                name_list.append(entry[0])
            if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")

    # ============ face recognition ==================

    def face_recog(self):
        # def draw_text_with_outline(img, text, position, font, font_scale, color, thickness=3, outline_color=(0, 0, 0)):
        #     # Draw the outline (black or contrasting color)
        #     cv2.putText(img, text, (position[0] - 1, position[1] - 1), font, font_scale, outline_color, thickness + 1, cv2.LINE_AA)
        #     cv2.putText(img, text, position, font, font_scale, color, thickness, cv2.LINE_AA)


        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord = []

            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int((100*(1-predict/300)))

                conn=mysql.connector.connect(host="localhost",username="root",password="abcd1234",database="face_recognizer")            
                my_cursor=conn.cursor()

                #Name
                my_cursor.execute("SELECT Name FROM student WHERE Student_id="+str(id))
                n = my_cursor.fetchone()
                n="+".join(n)

                #Roll
                my_cursor.execute("SELECT Roll FROM student WHERE Student_id="+str(id))
                r = my_cursor.fetchone()
                r="+".join(r)

                #Dep
                my_cursor.execute("SELECT Dep FROM student WHERE Student_id="+str(id))
                d = my_cursor.fetchone()
                d="+".join(d)

                #id
                my_cursor.execute("SELECT Student_id FROM student WHERE Student_id="+str(id))
                i = my_cursor.fetchone()
                i="+".join(i)


                if confidence > 75:

                    cv2.putText(img, f"ID: {i}",(x,y-100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)
                    cv2.putText(img, f"Roll: {r}",(x,y-70),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)
                    cv2.putText(img, f"Name: {n}",(x,y-40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)
                    cv2.putText(img, f"Department: {d}",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)
                    self.mark_attendance(i,r,n,d)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img, f"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)

                coord = [x, y, w, h]


            return coord
        
        def recognize(img, clf, faceCasCade):
            coord = draw_boundary(img, faceCasCade, 1.05, 10, (255,255,255),"Face", clf)
            return img
        
        faceCasCade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifiers.xml")

        video_cap = cv2.VideoCapture(0)
        
        if not video_cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            return

        while True:
            ret,img = video_cap.read()
            img=recognize(img, clf, faceCasCade)
            cv2.imshow("Welcome to Face Recognition", img)

            if cv2.waitKey(1) == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()
            

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()