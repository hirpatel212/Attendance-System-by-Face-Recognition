from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector 
import cv2



class Developer:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        
        #Title
        title_lbl = Label(self.root, text="DEVELOPER ",font=("times new roman", 35, "bold"), bg="white", fg="maroon")
        title_lbl.place(x=0, y=0,width=1530,height=45)

        #Image 1
        img_top = Image.open("images/devBG.jpeg").resize((1530, 570), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        

        f_lbl1 = Label(self.root, image=self.photoimg_top)
        f_lbl1.place(x=5, y=45, width=1530, height=570)

        #Frame
        img_top2 = Image.open("images/devBG.jpeg").resize((1530, 300), Image.LANCZOS)
        self.photoimg_top2 = ImageTk.PhotoImage(img_top2)
        f_lbl2 = Label(self.root, image=self.photoimg_top2)
        f_lbl2.place(x=5, y=600, width=1530, height=300)

        main_frame = Frame(f_lbl2, bd=2, bg="AliceBlue")
        main_frame.place(x=0, y=0, width=1530, height=300)

        dev_label=Label(main_frame,text="Hello we are the team of developers",font=("times new roman",20,"bold"),fg="black")
        dev_label.place(x=580,y=5)

        
if __name__ == "__main__":
    root = Tk()
    obj = Developer(root)
    root.mainloop()