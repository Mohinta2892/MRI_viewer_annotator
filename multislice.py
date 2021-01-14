import nibabel 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *


# Black background
plt.style.use('dark_background')

# Read the image 
img = nibabel.load('/mnt/wwn-0x5000c500cc87eb78/samia_data/FOR_SAMIA_LABELLED_SEQUENCES/biobank_seg/T1/T1_bb_0.nii.gz')

# Get a plain NumPy array, without all the metadata
x=np.asanyarray(img.dataobj)

# Header
header=img.header

# Set NAN to 0
x[np.isnan(x)] = 0

root = Tk()

### PREPARE SOME PARAMETERS ###

# Spacing for Aspect Ratio
sX=header['pixdim'][1]
sY=header['pixdim'][2]
sZ=header['pixdim'][3]


# Size per slice
lX = x.shape[0]
lY = x.shape[1]
lZ = x.shape[2]

# Middle slice number
mX = int(lX/2)
mY = int(lY/2)
mZ = int(lZ/2)

# True middle point
tmX = lX/2.0
tmY = lY/2.0
tmZ = lZ/2.0

def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)
                
### ORIENTATION ###
qfX = img.get_qform()[0,0]
sfX = img.get_sform()[0,0]

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

def plot_text():
    plt.text(lX+15,0, 'Press f for Flair', fontsize=7)
    plt.text(lX+15,10, 'Press 1 for T1', fontsize=7)
    plt.text(lX+15,20, 'Press c for T1CE', fontsize=7)
    plt.text(lX+15,30, 'Press 2 for T2', fontsize=7)
    plt.text(lX+15,40, 'Press s for T2STAR/T2*', fontsize=7)
    plt.text(lX+15,60, 'Press g to change to Sagittal view', fontsize=7)
    plt.text(lX+15,70, 'Press a to change to Axial view', fontsize=7)


def multi_slice_viewer_coronal(volume):
    remove_keymap_conflicts({'f', '1', '2', 's', 'c', 'a', 'g'})
    fig, ax = plt.subplots(facecolor='black',
    figsize=(7,4),
    dpi=200)
    
    ax.volume = volume
    #ax.index = volume.shape[0] // 2
    ax.index = mY
    imgplot = plt.imshow(
    np.rot90(x[:,mY,:]),
    aspect=sZ/sX)
    #imgplot = ax.imshow(np.rot90(volume[ax.index]),aspect=sZ/sX)
    imgplot.set_cmap('gray')
    ax.hlines(tmZ, 0, lX, colors='red', linestyles='dotted', linewidth=.5)
    ax.vlines(tmX, 0, lZ, colors='red', linestyles='dotted', linewidth=.5)
    plot_text()

    plt.axis('off')

    fig.canvas.mpl_connect('key_press_event', process_key)
    fig.canvas.mpl_connect('scroll_event', lambda event: process_scrollbar(event, 'c'))
    # plt.show()

def multi_slice_viewer_sagittal(volume):
    remove_keymap_conflicts({'f', '1'})

    fig, ax = plt.subplots(facecolor='black',
                           figsize=(7, 4),
                           dpi=200)

    ax.volume = volume
    # ax.index = volume.shape[0] // 2
    ax.index = mX
    imgplot = plt.imshow(
        np.rot90(x[mX, :, :]),
        aspect=sZ / sY)
    # imgplot = ax.imshow(np.rot90(volume[ax.index]),aspect=sZ/sX)
    imgplot.set_cmap('gray')
    ax.hlines(tmZ, 0, lY, colors='red', linestyles='dotted', linewidth=.5)
    ax.vlines(tmY, 0, lZ, colors='red', linestyles='dotted', linewidth=.5)
    plot_text()

    plt.axis('off')

    fig.canvas.mpl_connect('key_press_event', process_key)
    fig.canvas.mpl_connect('scroll_event', lambda event: process_scrollbar(event, 'g'))


    plt.show()


def multi_slice_viewer_axial(volume):
    remove_keymap_conflicts({'f', '1'})
    fig, ax = plt.subplots(facecolor='black',
                           figsize=(7, 4),
                           dpi=200)

    ax.volume = volume
    # ax.index = volume.shape[0] // 2
    ax.index = mZ
    imgplot = plt.imshow(
        np.rot90(x[:, :, mZ]),
        aspect=sY / sX)
    # imgplot = ax.imshow(np.rot90(volume[ax.index]),aspect=sZ/sX)
    imgplot.set_cmap('gray')
    ax.hlines(tmY, 0, lX, colors='red', linestyles='dotted', linewidth=.5)
    ax.vlines(tmX, 0, lY, colors='red', linestyles='dotted', linewidth=.5)
    plot_text()

    plt.axis('off')

    fig.canvas.mpl_connect('key_press_event', process_key)
    fig.canvas.mpl_connect('scroll_event', lambda event: process_scrollbar(event, 'a'))
    plt.show()

def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'f':
        print('key pressed f')
        plt.close(fig)

    elif event.key == '1':
        print('key pressed 1')
        plt.close(fig)

    elif event.key == 'c':
        print('key pressed c')
        plt.close(fig)

    elif event.key == '2':
        print('key pressed 2')
        plt.close(fig)

    elif event.key == 's':
        print('key pressed s')
        plt.close(fig)

    elif event.key == 'g':
        print('key pressed g')
        # plt.close(plt.gcf())
        multi_slice_viewer_sagittal(x)

    elif event.key == 'a':
        print('key pressed a')
        # plt.close()
        multi_slice_viewer_axial(x)

def process_scrollbar(event, view_option):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.button == 'down' and view_option=='c':
        previous_slice(ax, view_option)
    elif event.button == 'up' and view_option=='c':
        next_slice(ax, view_option)
    elif event.button == 'down' and view_option=='g':
        previous_slice(ax, view_option)
    elif event.button == 'up' and view_option=='g':
        next_slice(ax, view_option)
    elif event.button == 'down' and view_option=='a':
        previous_slice(ax, view_option)
    elif event.button == 'up' and view_option=='a':
        next_slice(ax, view_option)
    fig.canvas.draw()

def previous_slice(ax, view_option):
    volume = ax.volume
    if view_option=='c':
        ax.index = (ax.index - 1) % lY   # wrap around using %
        ax.images[0].set_array(np.rot90(x[:,ax.index,:]))
    elif view_option=='g':
        ax.index = (ax.index - 1) % lX   # wrap around using %
        ax.images[0].set_array(np.rot90(x[ax.index, :, :]))
    elif view_option=='a':
        ax.index = (ax.index - 1) % lZ   # wrap around using %
        ax.images[0].set_array(np.rot90(x[:, :, ax.index]))

def next_slice(ax, view_option):
    volume = ax.volume
    if view_option=='c':
        ax.index = (ax.index + 1) % lY   # wrap around using %
        ax.images[0].set_array(np.rot90(x[:,ax.index,:]))
    elif view_option=='g':
        ax.index = (ax.index + 1) % lX   # wrap around using %
        ax.images[0].set_array(np.rot90(x[ax.index, :, :]))
    elif view_option=='a':
        ax.index = (ax.index + 1) % lZ   # wrap around using %
        ax.images[0].set_array(np.rot90(x[:, :, ax.index]))

    
multi_slice_viewer_coronal(x)
plt.show()


