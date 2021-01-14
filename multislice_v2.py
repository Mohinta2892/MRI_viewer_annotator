import nibabel
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import sys

class MultiSliceViewer:

    def __init__(self, input_img=None, label_unknown=None):

        # Black background
        plt.style.use('dark_background')

        # Read the image
        try:
            img = nibabel.load(input_img)
            self.image_name=input_img
            self.label_unknown= label_unknown
        except Exception as e:
            print('Load image error: ', e)

        # Get a plain NumPy array, without all the metadata
        self.x = np.asanyarray(img.dataobj)

        # Header
        header = img.header

        # Set NAN to 0
        self.x[np.isnan(self.x)] = 0

        ### PREPARE SOME PARAMETERS ###

        # Spacing for Aspect Ratio
        self.sX = header['pixdim'][1]
        self.sY = header['pixdim'][2]
        self.sZ = header['pixdim'][3]

        # Size per slice
        self.lX = self.x.shape[0]
        self.lY = self.x.shape[1]
        self.lZ = self.x.shape[2]

        # Middle slice number
        self.mX = int(self.lX / 2)
        self.mY = int(self.lY / 2)
        self.mZ = int(self.lZ / 2)

        # True middle point
        self.tmX = self.lX / 2.0
        self.tmY = self.lY / 2.0
        self.tmZ = self.lZ / 2.0

        ### ORIENTATION ###
        qfX = img.get_qform()[0, 0]
        sfX = img.get_sform()[0, 0]

        if qfX < 0 and (sfX == 0 or sfX < 0):
            oL = 'R'
            oR = 'L'
        elif qfX > 0 and (sfX == 0 or sfX > 0):
            oL = 'L'
            oR = 'R'
        if sfX < 0 and (qfX == 0 or qfX < 0):
            oL = 'R'
            oR = 'L'
        elif sfX > 0 and (qfX == 0 or qfX > 0):
            oL = 'L'
            oR = 'R'

        # To record input
        self.record_input = ''

    def remove_keymap_conflicts(self, new_keys_set):
        for prop in plt.rcParams:
            if prop.startswith('keymap.'):
                keys = plt.rcParams[prop]
                remove_list = set(keys) & new_keys_set
                for key in remove_list:
                    keys.remove(key)

    def plot_text(self):
        text = (
                'Press f for Flair' + "\n"
                + 'Press 1 for T1' + "\n"
                + 'Press c for T1CE' + "\n"
                +  'Press 2 for T2' + "\n"
                + 'Press s for T2STAR/T2*' + "\n\n"
                +  'Press u/SPACEBAR if unknown' + "\n"
                + 'Press q to exit' + "\n\n"
                + 'You may click on each subplot \nand scroll to change the slices' +"\n"
        )

        # plt.text(-300, 300, 'You may click on each subplot and scroll to change the slices', fontsize=7)
        return text

    def multi_slice_viewer(self):
        self.remove_keymap_conflicts({'f', '1', '2', 's', 'c', 'u', 'q'})
        fig = plt.figure(
            facecolor='black',
            figsize=(8, 4),
            dpi=200
        )
        self.ax1 = fig.add_subplot(1, 4, 1)
        self.ax1.index = self.mY
        imgplot = plt.imshow(
            np.rot90(self.x[:, self.mY, :]),
            aspect=self.sZ / self.sX)
        # imgplot = ax.imshow(np.rot90(volume[ax.index]),aspect=sZ/sX)
        imgplot.set_cmap('gray')
        self.ax1.hlines(self.tmZ, 0, self.lX, colors='red', linestyles='dotted', linewidth=.5)
        self.ax1.vlines(self.tmX, 0, self.lZ, colors='red', linestyles='dotted', linewidth=.5)
        plt.axis('off')

        self.ax2 = fig.add_subplot(1, 4, 2)
        self.ax2.index = self.mX
        imgplot = plt.imshow(
            np.rot90(self.x[self.mX, :, :]),
            aspect=self.sZ / self.sY)
        imgplot.set_cmap('gray')
        self.ax2.hlines(self.tmZ, 0, self.lY, colors='red', linestyles='dotted', linewidth=.5)
        self.ax2.vlines(self.tmY, 0, self.lZ, colors='red', linestyles='dotted', linewidth=.5)
        plt.axis('off')

        self.ax3 = fig.add_subplot(1, 4, 3)
        self.ax3.index = self.mZ
        imgplot = plt.imshow(
            np.rot90(self.x[:, :, self.mZ]),
            aspect=self.sY / self.sX)
        imgplot.set_cmap('gray')
        self.ax3.hlines(self.tmY, 0, self.lX, colors='red', linestyles='dotted', linewidth=.5)
        self.ax3.vlines(self.tmX, 0, self.lY, colors='red', linestyles='dotted', linewidth=.5)

        plt.axis('off')
        text=self.plot_text()

        self.ax4 = fig.add_subplot(1, 4, 4)
        plt.text(0.15, 0.95, text, horizontalalignment='left', verticalalignment='top', size=6, color='white',)
        plt.axis('off')

        if self.label_unknown is None:
            fig.suptitle(f'Is this a {self.image_name.split("/")[-2]} ?')
        else:
            fig.suptitle(f'Is this a {self.image_name.split("/")[-2]} ? (previously labelled unknown)')

        fig.canvas.mpl_connect("button_press_event", lambda event: self.onclick_select(event, fig))
        fig.canvas.mpl_connect('key_press_event', self.process_key)

        plt.show()

    def onclick_select(self, event, fig):
        # print(event.inaxes)

        if event.inaxes == self.ax1:
            fig.canvas.mpl_connect('key_press_event', self.process_key)
            fig.canvas.mpl_connect('scroll_event', lambda event: self.process_scrollbar(event, 'c'))
            flag_ax2 = False
            flag_ax3 = False
        elif event.inaxes == self.ax2:
            fig.canvas.mpl_connect('key_press_event', self.process_key)
            fig.canvas.mpl_connect('scroll_event', lambda event: self.process_scrollbar(event, 'g'))
            flag_ax1 = False
            flag_ax3 = False
        elif event.inaxes == self.ax3:
            fig.canvas.mpl_connect('key_press_event', self.process_key)
            fig.canvas.mpl_connect('scroll_event', lambda event: self.process_scrollbar(event, 'a'))



    def process_key(self, event):
        fig = event.canvas.figure
        if event.key == 'f':
            self.record_input='FLAIR'
            plt.close(fig)

        elif event.key == '1':
            self.record_input='T1'
            plt.close(fig)

        elif event.key == 'c':
            self.record_input='T1CE'
            plt.close(fig)

        elif event.key == '2':
            self.record_input='T2'
            plt.close(fig)

        elif event.key == 's':
            self.record_input='T2STAR'
            plt.close(fig)

        elif event.key == 'u':
            self.record_input='Unknown'
            plt.close(fig)

        elif event.key == ' ':
            self.record_input='Unknown'
            plt.close(fig)

        elif event.key == 'q':
            self.record_input='q'
            plt.close(fig)
            # sys.exit()



    def process_scrollbar(self, event, view_option):
        fig = event.canvas.figure
        if event.button == 'down' and view_option == 'c' and event.inaxes == self.ax1:
            ax = fig.axes[0]
            self.previous_slice(ax, view_option)
        elif event.button == 'up' and view_option == 'c' and event.inaxes == self.ax1:
            ax = fig.axes[0]
            self.next_slice(ax, view_option)
        elif event.button == 'down' and view_option == 'g' and event.inaxes == self.ax2:
            ax = fig.axes[1]
            self.previous_slice(ax, view_option)
        elif event.button == 'up' and view_option == 'g' and event.inaxes == self.ax2:
            ax = fig.axes[1]
            self.next_slice(ax, view_option)
        elif event.button == 'down' and view_option == 'a' and event.inaxes == self.ax3:
            ax = fig.axes[2]
            self.previous_slice(ax, view_option)
        elif event.button == 'up' and view_option == 'a' and event.inaxes == self.ax3:
            ax = fig.axes[2]
            self.next_slice(ax, view_option)
        fig.canvas.draw()


    def previous_slice(self, ax, view_option):
        if view_option == 'c':
            ax.index = (ax.index - 1) % self.lY  # wrap around using %
            ax.images[0].set_array(np.rot90(self.x[:, ax.index, :]))
        elif view_option == 'g':
            ax.index = (ax.index - 1) % self.lX  # wrap around using %
            ax.images[0].set_array(np.rot90(self.x[ax.index, :, :]))
        elif view_option == 'a':
            ax.index = (ax.index - 1) % self.lZ  # wrap around using %
            ax.images[0].set_array(np.rot90(self.x[:, :, ax.index]))


    def next_slice(self, ax, view_option):
        if view_option == 'c':
            ax.index = (ax.index + 1) % self.lY  # wrap around using %
            ax.images[0].set_array(np.rot90(self.x[:, ax.index, :]))
        elif view_option == 'g':
            ax.index = (ax.index + 1) % self.lX  # wrap around using %
            ax.images[0].set_array(np.rot90(self.x[ax.index, :, :]))
        elif view_option == 'a':
            ax.index = (ax.index + 1) % self.lZ  # wrap around using %
            ax.images[0].set_array(np.rot90(self.x[:, :, ax.index]))




# for i in range(5):
#     img='/mnt/wwn-0x5000c500cc87eb78/samia_data/FOR_SAMIA_LABELLED_SEQUENCES/biobank_seg/T1/T1_bb_0.nii.gz'
#
#     view=MultiSliceViewer(img)
#     view.multi_slice_viewer()


