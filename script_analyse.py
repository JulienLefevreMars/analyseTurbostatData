import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Utils.temporal_series as ts
from os import stat
from datetime import datetime
import Utils.time_information as ti
from Utils.data_extraction import get_filenames
import sys


if __name__ == "__main__":
    NB_LINES_HEADER=68

    try:
        folder=sys.argv[1]
    except:
        folder = '/home/julienlefevre/ownCloud/Documents/EcoInfo/Projects/Ecodiag/Voltcraft/2020_06_16/1/'
        #folder = 'Data/'

    (filename1,filename2)=get_filenames(folder)

    #-------------------------#
    # Read the turbostat Data #
    #-------------------------#

    data = pd.read_csv(filename1, sep=None, skiprows=range(0, NB_LINES_HEADER))
    #data = pd.read_csv(filename1, delimiter=',') # skip the header (Sophie)
    time1 = stat(filename1).st_mtime  # Modification time

    number_of_proc = 9
    index_of_proc = 0
    time_per_step = 1
    number_of_steps1 = int((data.shape[0]+1)/(number_of_proc+1))
    columns = [46, 47, 48, 49]
    # columns=[42,43,44,45] # columns for Sophie

    signal=np.zeros((number_of_steps1,len(columns)))  # assumes 1min per acquisiton
    for (i, column) in enumerate(columns):
        signal[:,i]=data.iloc[index_of_proc+(number_of_proc+1)*np.array([i for i in range(number_of_steps1)]),column]

    #-------------------------#
    # Read the Voltcraft info #
    #-------------------------#

    data2 = pd.read_csv(filename2, sep=None)
    time_per_step2 = 1  # 1min per step
    number_of_steps2 = data2.shape[0]
    #time2 = stat(filename2).st_mtime # modification time (seconds) => WARNING: time of the .csv, not the .BIN file
    starttime = ti.str_to_timestamp(data2.iloc[0,0])
    time2 = starttime + number_of_steps2 *60

    #--------------------------------------------#
    # Figure with Voltcraft and turbostat values #
    #--------------------------------------------#

    steps1 = - np.arange(number_of_steps1)[::-1] + time1//60
    steps2 = - np.arange(number_of_steps2)[::-1] + time2//60

    plt.figure()
    plt.title('Turbostat information vs Voltcraft wattmeter')
    plt.plot(steps1,signal)
    plt.grid()
    plt.ylabel('Watts')
    plt.xlabel('Time (min)')
    plt.plot(steps2,np.array(data2.iloc[:,4]))
    plt.legend(data.keys()[columns].append(pd.Index(['Voltcraft'])))
    xticklabels = plt.gca().get_xticks()

    labels=[]
    for i,x in enumerate(xticklabels):
        time_x=datetime.fromtimestamp(plt.gca().get_xticks()[i] * 60)
        labels.append(str(time_x.hour)+'H'+str(time_x.minute))

    plt.gca().set_xticklabels(labels)
    plt.show()


