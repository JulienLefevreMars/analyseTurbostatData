import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import temporal_series as ts
from os import stat
from datetime import datetime

if __name__ == "__main__":
    # You need to run first turbostat, e.g. with
    # sudo turbostat --interval 10 --quiet -out ThirdTest.out
    NB_LINES_HEADER=68

    # Then read the Data
    folder='/home/julienlefevre/ownCloud/Documents/EcoInfo/Projects/Ecodiag/Voltcraft/2020_06_16/1/'
    filename = folder+ "2020_06_16_10H01.out"
    data = pd.read_csv(filename, delimiter='\t',skiprows=range(0,NB_LINES_HEADER))
    time = datetime.fromtimestamp(stat(filename).st_mtime) # Modification time

    number_of_proc=9
    index_of_proc=0
    time_per_step=1
    number_of_steps=int((data.shape[0]+1)/(number_of_proc+1))-1
    columns=[46,47,48,49]

    signal=np.zeros(((number_of_steps+1),len(columns))) # assumes 1 s per acquisiton
    for (i,column) in enumerate(columns):
        signal[:,i]=data.iloc[index_of_proc+(number_of_proc+1)*np.array([i for i in range(number_of_steps+1)]),column]
        #signal[:,i]=ts.averaging(np.array(signal_orig,dtype=float),60)

    #time=np.linspace(0,time_per_step*(number_of_steps),number_of_steps+1)
    #for column in columns:
    #    plt.plot(time,np.array(data.iloc[index_of_proc+(number_of_proc+1)*np.array([i for i in range(number_of_steps+1)]),column],dtype=float))

    # Read the Voltcraft info
    filename2 = folder + 'el4kcsv_202006160749.csv'
    data2 = pd.read_csv(filename2, delimiter=',')
    time2 = datetime.fromtimestamp(stat(filename2).st_mtime) # Modification time

    time_per_step2 = 1  # 1min per step
    number_of_steps2 = data2.shape[0]

    # Register
    t1=200
    t2=300
    tstart=240
    tend=340
    correlations=ts.register(signal[tstart:tend,0],np.array(data2.iloc[:,4]),t1,t2)
    tshift=np.argmax(correlations)

    # Figure, without registration
    #steps2=np.linspace(0,time_per_step2*(number_of_steps2-1),number_of_steps2)

    plt.figure()
    plt.title('Before temporal registration')
    plt.plot(signal)
    plt.grid()
    plt.ylabel('Watts')
    plt.xlabel('Time (min)')
    plt.plot(time2,np.array(data2.iloc[:,4]))
    plt.legend(data.keys()[columns].append(pd.Index(['Voltcraft'])))

    rect=plt.Rectangle((tstart,0),tend-tstart,np.array(data2.iloc[:,4]).max(),facecolor=[0.5,0.8,0.9])
    plt.gca().add_patch(rect)

    plt.figure()
    plt.plot(np.arange(t1,t2)-tstart,correlations)
    plt.xlabel('Temporal shift')
    plt.ylabel('Correlation')

    # Figure, after registration
    time1=t1+tshift+np.arange(0,len(signal))-tstart

    plt.figure()
    plt.title('After temporal registration')
    plt.plot(time1,signal)
    plt.grid()
    plt.ylabel('Watts')
    plt.xlabel('Time (min)')
    plt.plot(time2,np.array(data2.iloc[:,4]))
    plt.legend(data.keys()[columns].append(pd.Index(['Voltcraft'])))

