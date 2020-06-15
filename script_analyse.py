import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import temporal_series as ts

if __name__ == "__main__":
    # You need to run first turbostat, e.g. with
    # sudo turbostat --interval 10 --quiet -out ThirdTest.out

    # Then read the Data
    #data=pd.read_csv("FirstTest.out",delimiter='\t')
    folder='/home/julienlefevre/ownCloud/Documents/EcoInfo/Projects/Ecodiag/Voltcraft/2020_06_11/'

    data = pd.read_csv(folder+ "2020_06_11_remove_header.out", delimiter='\t')  
    number_of_proc=9
    index_of_proc=0
    time_per_step=1
    number_of_steps=int((data.shape[0]+1)/(number_of_proc+1))-1
    columns=[46,47,48,49]

    signal=np.zeros(((number_of_steps+1)//60,len(columns))) # assumes 1 s per acquisiton
    for (i,column) in enumerate(columns):
        signal_orig=data.iloc[index_of_proc+(number_of_proc+1)*np.array([i for i in range(number_of_steps+1)]),column]
        signal[:,i]=ts.averaging(np.array(signal_orig,dtype=float),60)

    #time=np.linspace(0,time_per_step*(number_of_steps),number_of_steps+1)
    #for column in columns:
    #    plt.plot(time,np.array(data.iloc[index_of_proc+(number_of_proc+1)*np.array([i for i in range(number_of_steps+1)]),column],dtype=float))

    # Read the Voltcraft info
    data2 = pd.read_csv(folder + 'el4kcsv_202006120752.csv', delimiter=';')
    time_per_step2 = 1  # 1min per step
    number_of_steps2 = data2.shape[0]

    # Figure, without registration
    time2=np.linspace(0,time_per_step2*(number_of_steps2-1),number_of_steps2)

    plt.figure()
    plt.title('Before temporal registration')
    plt.plot(signal)
    plt.grid()
    plt.ylabel('Watts')
    plt.xlabel('Time (min)')
    plt.plot(time2,np.array(data2.iloc[:,4]))
    plt.legend(data.keys()[columns].append(pd.Index(['Voltcraft'])))

    # Register
    t1=200
    t2=300
    tstart=240
    tend=340
    correlations=ts.register(signal[tstart:tend,0],np.array(data2.iloc[:,4]),t1,t2)
    tshift=np.argmax(correlations)

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

