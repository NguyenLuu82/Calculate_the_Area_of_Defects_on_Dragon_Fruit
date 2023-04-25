from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os
from cv2 import resize

from matplotlib.ft2font import BOLD
import Find_defects as fd
import cv2

from tkinter import Tk, Label, BOTH
from tkinter.ttk import Frame, Style

class main():
    def __init__(self):
        #khoi tao giao dien
        self.root = Tk()
        self.root.title("Detects Dragon Fruits")
        self.root.geometry("900x640")
        self.root.attributes('-topmost', False) #code lam cho cua so lam viec luon tren top
        Tk_Width = 1000
        Tk_Height = 1000
        x_Left = int(self.root.winfo_screenwidth()/2 - Tk_Width/2)
        y_Top = int(self.root.winfo_screenheight()/2 - Tk_Height/2)
        self.root.geometry("+{}+{}".format(x_Left, y_Top))
    
        #label
        self.label_title = Label(text= "NGUYEN VAN LUU_19146355_CLASS_07", bg= "yellow", font= BOLD)
        self.label_title.place(x=0,y=0,width=900,height=40)

        self.label_defects = Label(text= "", bg= "white")
        self.label_defects.place(x=0,y=600,width=110,height=40)
        self.label_defects = Label(text="Original", bg= "yellow", font= BOLD)
        self.label_defects.place(x=110,y=600,width=234,height=40)
        self.label_mask = Label(text= "Defected", bg= "green", font= BOLD)
        self.label_mask.place(x=344,y=600,width=234,height=40)
        self.label_defects = Label(text= "Masked", bg= "red", font= BOLD)
        self.label_defects.place(x=578,y=600,width=234,height=40)
        self.label_defects = Label(text= "", bg= "white")
        self.label_defects.place(x=812,y=600,width=88,height=40)

        self.label_mask = Label(text= "Button", bg= "pink", font= BOLD)
        self.label_mask.place(x=45,y=40,width=220,height=40)
        self.label_mask = Label(text= "Input", bg= "pink", font= BOLD)
        self.label_mask.place(x=330,y=40,width=220,height=40)

        #Open:
        self.open_img= Button(text='Open',bg= "pink",bd= 5, activebackground = 'green', font= BOLD, command=self.onOpen)
        self.open_img.place(x=45,y=90,width=220,height=100)

        #Defects:
        self.defects = Button(text='Defects',bg= "pink",bd= 5, activebackground = 'blue',font= BOLD, command=self.onDefects)
        self.defects.place(x=45,y=200,width=220,height=100)
        
        #Logo
        logo = Image.open("logo.jpg")
        resize = logo.resize((260,260), Image.ANTIALIAS)
        bardejov = ImageTk.PhotoImage(resize)
        label1 = Label(image=bardejov)
        label1.image = bardejov
        label1.place(x=600, y=40)
    
    #open Image: 
    def openfn(self):
        filename = filedialog.askopenfilename(title='open')
        return filename
    def onOpen(self):
        global x
        global original
        x = self.openfn()
        img = Image.open(x)
        img = img.resize((220, 220), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        original = Label(image=img).place(x=330,y=80)
        original.image = img
        original.pack()
    
    #onDefects    
    def onDefects(self):
        global imgout
        imgin = cv2.imread(x,cv2.IMREAD_COLOR)
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2RGB)
        fd.Find_defects(imgin)
        img_defect = (Image.open("imgout.jpg"))
        resize = img_defect.resize((900,300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resize)
        lab   = Label(image=photo).place(x=0,y=300)
        lab.image = photo
        lab.pack()
        
    def load(self):
        self.root.mainloop()
#running.....
form = main()
form.load()