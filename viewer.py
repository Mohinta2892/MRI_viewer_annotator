'''
Author: Samia Mohinta
A python based MRI viewer, that helps to annotate sequence types with a click of a key.
It can save results (intermediate as well, if you quit mid way) into a csv file.
You can skip labellling of a specific sequence and repeat those for labelling later on.
'''

import multislice_v2 as mview
import sys, getopt
import os
import pandas as pd
import numpy as np


class Viewer:

    def __init__(self, input_dir_path=None, input_pred_csv=None,  file_extensions=('nii', 'nii.gz'), repeat_unlabelled_images=True):

        if input_dir_path is not None:
            index_array = []
            filelist = []
            pred_seq_list = []
            corrected_seq_list = []
            for paths, dirs, files in os.walk(input_dir_path):
                for file in files:
                    if file.endswith(file_extensions):
                        index_array.append(os.sep.join([paths, file]))
            for img in index_array:
                view = mview.MultiSliceViewer(img)
                view.multi_slice_viewer()
                if view.record_input != 'q':
                    filelist.append(img)
                    pred_seq_list.append(img.split('/')[-2])
                    corrected_seq_list.append(view.record_input)
                else:
                    break

            self.df = pd.DataFrame({'file': filelist, 'predicted_sequence': pred_seq_list, 'corrected_sequence': corrected_seq_list})

            if repeat_unlabelled_images:

                for index, row in self.df.iterrows():
                    if row['corrected_sequence'] == 'Unknown':
                        view = mview.MultiSliceViewer(row['file'], label_unknown=row['corrected_sequence'])
                        view.multi_slice_viewer()
                        if view.record_input !='q':
                            row.iloc[2]=view.record_input
                        else:
                            break

            self.df.to_csv('new_manual_corrections.csv', index=False)

        elif input_pred_csv is not None:
            pass


def main(inputdirpath=None, inputcsvfile=None, repeat_unlabelled_images=False):
    view = Viewer(input_dir_path=inputdirpath, input_pred_csv=inputcsvfile, repeat_unlabelled_images=repeat_unlabelled_images)


if __name__ == "__main__":

    ##default settings##
    inputdirpath= '/mnt/wwn-0x5000c500cc8a8151/Prototype_folder_structure/HEAD/T1/VANILLA_T1/REGISTERED/SKULLS_OASIS' #/mnt/wwn-0x5000c500cc87eb78/subset_allcombo'
    inputcsvfile=None
    repeat_unlabelled_images = False #Change to true if previously marked unknown images need to be repeated
    main(inputdirpath, inputcsvfile, repeat_unlabelled_images)