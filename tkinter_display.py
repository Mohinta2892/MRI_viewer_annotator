import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, Tk, Toplevel


root = Tk()
window = Toplevel(root)
#window = tk.Toplevel()
window.title("SEE image and ENTER its information")
window.geometry("800x800") # You can drop this line if you want.
window.configure(background='grey')

#path = "/mnt/wwn-0x5000c500cc8a8151/Awesome-Free-Butterfly-Background-Download.jpg"
path = "/mnt/wwn-0x5000c500cc8a8151/nifti_image_generator-master/disp_head.jpeg"
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image = img)

txtVar = tk.StringVar(None)
usrIn = tk.Entry(window, textvariable = txtVar, width = 90)
usrIn.grid(row = 50, column = 60)



usrIn.pack()
panel.pack()


window.mainloop()
