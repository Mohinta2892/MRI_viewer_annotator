from tkinter import Button, Frame, Tk, Label  # Python 3
#from Tkinter import Button, Frame, Tk    # Python 2
from PIL import ImageTk, Image
class MyClass:
    def __init__(self, master):
    
       self.path = "/mnt/wwn-0x5000c500cc8a8151/nifti_image_generator-master/disp_head.jpeg"
       self.img = ImageTk.PhotoImage(Image.open(self.path))
       self.panel = Label(master, image = self.img)
       #self.panel.pack()
    
       self.panel.grid(row =2, column=0, padx=5,pady=5)

       frame = Frame(master)
       frame.grid(row=1, column=0, columnspan=5)        

       self.button_flair = Button(frame, text="press f for flair", command=self.func_flair).grid(row=0, column=0)
       #self.button_flair.pack(side='left')
       master.bind('f', self.func_flair)
       
       self.button_t1 = Button(frame, text="press 1 for t1", command=self.func_t1).grid(row=0, column=1)
       master.bind('1', self.func_t1)
       
       self.button_t2 = Button(frame, text="press 2 for t2", command=self.func_t2).grid(row=0, column=2)
       master.bind('2', self.func_t1)
       
    def func_flair(self, _event=None):
        user_in='FLAIR'
        root.destroy()
        
    def func_t1(self, _event=None):
        user_in='T1'
        root.destroy()
        
    def func_t2(self, _event=None):
        user_in='T2'
        root.destroy()

root = Tk()
root.title("SEE image and ENTER its information")
abc = MyClass(root)
root.mainloop()
