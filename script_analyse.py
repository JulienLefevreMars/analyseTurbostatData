import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    #Data
    data=pd.read_csv("FirstTest.out",delimiter='\t')

    number_of_proc=9
    index_of_proc=0
    number_of_steps=int((data.shape[0]+1)/(number_of_proc+1))-1
    columns=[46,47,48,49]

    time=np.linspace(0,20*(number_of_steps),number_of_steps+1)
    #for index_of_proc in range(number_of_proc):
    for column in columns:
        plt.plot(time/60,np.array(data.iloc[index_of_proc+(number_of_proc+1)*np.array([i for i in range(number_of_steps+1)]),column],dtype=float))

    plt.grid()
    plt.legend(data.keys()[columns])
    plt.ylabel('Watts')
    plt.xlabel('Time (min)')
