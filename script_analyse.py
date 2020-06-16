import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import temporal_series as ts
from os import stat
from datetime import datetime
import time_information as ti

if __name__ == "__main__":
    # You need to run first turbostat, e.g. with
    # sudo turbostat --interval 60 --quiet -out Test.out
    NB_LINES_HEADER=68

    # Then read the Data
    folder='/home/julienlefevre/ownCloud/Documents/EcoInfo/Projects/Ecodiag/Voltcraft/2020_06_16/1/'
    filename = folder+ "2020_06_16_10H01.out"
    data = pd.read_csv(filename, delimiter='\t',skiprows=range(0,NB_LINES_HEADER))
    time1 = stat(filename).st_mtime # Modification time
    #time = datetime.fromtimestamp(stat(filename).st_mtime) # Modification time

    number_of_proc=9
    index_of_proc=0
    time_per_step=1
    number_of_steps1=int((data.shape[0]+1)/(number_of_proc+1))
    columns=[46,47,48,49]

    signal=np.zeros((number_of_steps1,len(columns))) # assumes 1 s per acquisiton
    for (i,column) in enumerate(columns):
        signal[:,i]=data.iloc[index_of_proc+(number_of_proc+1)*np.array([i for i in range(number_of_steps1)]),column]

    #time=np.linspace(0,time_per_step*(number_of_steps),number_of_steps+1)
    #for column in columns:
    #    plt.plot(time,np.array(data.iloc[index_of_proc+(number_of_proc+1)*np.array([i for i in range(number_of_steps+1)]),column],dtype=float))

    # Read the Voltcraft info
    filename2 = folder + 'el4kcsv_202006160749.csv'
    data2 = pd.read_csv(filename2, delimiter=',')
    time_per_step2 = 1  # 1min per step
    number_of_steps2 = data2.shape[0]
    #time2 = stat(filename2).st_mtime # modification time (seconds) => WARNING: time of the .csv, not the .BIN file
    #time2 = datetime.fromtimestamp(stat(filename2).st_mtime) # Modification time
    starttime = ti.str_to_timestamp(data2.iloc[0,0])
    time2 = starttime + number_of_steps2 *60



    # Figure with Voltcraft and turbostat values
    #steps2=np.linspace(0,time_per_step2*(number_of_steps2-1),number_of_steps2)
    time_lag=(time2-time1)//60
    steps1 = - np.arange(number_of_steps1)[::-1] + time1//60
    steps2 = - np.arange(number_of_steps2)[::-1] + time2//60

    plt.figure()
    plt.title('Before temporal registration')
    plt.plot(steps1,signal)
    plt.grid()
    plt.ylabel('Watts')
    plt.xlabel('Time (min)')
    plt.plot(steps2,np.array(data2.iloc[:,4]))
    plt.legend(data.keys()[columns].append(pd.Index(['Voltcraft'])))
    xticklabels=plt.gca().get_xticks()

    labels=[]
    for i,x in enumerate(xticklabels):
        time_x=datetime.fromtimestamp(plt.gca().get_xticks()[i] * 60)
        labels.append(str(time_x.hour)+'H'+str(time_x.minute))

    plt.gca().set_xticklabels(labels)


