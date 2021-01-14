import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import matplotlib.pyplot as plt


class Embed:

    def __init__(self, root_):
        self.root = root_
        self.a = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
        self.b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.c = np.array([[1, 4, 7], [4, 7, 10], [7, 10, 13]])
        self.ctuple = (self.a, self.b)
        self.cube = np.dstack(self.ctuple)
        self.cube = np.dstack([self.cube, self.c])
        self.plot = Plotting(self.root, self.cube)
        self.button = Tk.Button(root, text="check", command=lambda: self.plot.plot())
        self.button.pack()


class Plotting:
    def __init__(self, root, cube):
        self.root = root
        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111)
        self.cube = cube
        self.slider = Tk.Scale(
            self.root, from_=0, to=cube.shape[2] - 1, resolution=0.01, orient=Tk.HORIZONTAL, command=self.update
        )
        # self.slider.on_changed(self.update)
        self.slider.pack()
        self.plotted = False
        self.l = None
        self.canvas = None
        plt.show()

    def plot(self, **kwargs):
        self.plotted = True
        s = [slice(0, 1) if i == 2 else slice(None) for i in xrange(3)]
        im = self.cube[s].squeeze()
        self.l = self.ax.imshow(im, **kwargs)
        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    def update(self, val):
        ind = int(self.slider.get())
        s = [slice(ind, ind + 1) if i == 2 else slice(None) for i in range(3)]
        if self.plotted:
            im = self.cube[s].squeeze()
            self.l.set_data(im)
            self.canvas.draw()


if __name__ == '__main__':
    root = Tk.Tk()
    app = Embed(root)
    root.mainloop()
    root.destroy()