import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Utils.temporal_series as ts
import Utils.time_information as ti
from Utils.data_extraction import get_filenames
import sys
# import pwlf
import piecewise as pw


if __name__ == "__main__":
    NB_LINES_HEADER=68

    try:
        folder=sys.argv[1]
    except:
        folder = '/home/julienlefevre/ownCloud/Documents/EcoInfo/Projects/Ecodiag/Voltcraft/2020_06_16/1/'
        #folder = 'Data/'

    (filename1,filename2)=get_filenames(folder)

    # -------------------------#
    # Read the Voltcraft info  #
    # -------------------------#

    data2 = pd.read_csv(filename2, sep=None)
    time_per_step2 = 1  # 1min per step
    number_of_steps2 = data2.shape[0]
    starttime = ti.str_to_timestamp(data2.iloc[0, 0])
    time2 = starttime + number_of_steps2 * 60

    signal2 = np.array(data2.iloc[:,4])
    steps2 = - np.arange(number_of_steps2)[::-1] + time2//60

    # Detect discontinuity (battery on/off)
    indices = ts.detect_battery_off(signal2)

    #-----------------------#
    # Piecewise regression  #
    #-----------------------#

    n_clusters = 8 # ad hoc on this example

    x = np.arange(number_of_steps2).reshape((number_of_steps2,1))
    y = signal2.reshape((number_of_steps2,1))
    # # Solution 1: regression clustering -> no continuity in the points
    # clusters0 = np.zeros((number_of_steps2,1))
    # uniform_interval_length=number_of_steps2//n_clusters
    # for i in range(n_clusters):
    #     clusters0[i*uniform_interval_length:(i+1)*uniform_interval_length]=i
    # clusters0[(i+1)*uniform_interval_length:]=i
    #
    # clusters, A, b, energy = rc.greedyAlgorithm(x,y,n_clusters,clusters0)
    # rc.vizuClustersAndLines(x,y,clusters,n_clusters,A,b)

    # # Solution 2: piecewise linear fit -> discontinuity not available
    # # https://github.com/cjekel/piecewise_linear_fit_py
    # # See also
    # # https://www.datadoghq.com/blog/engineering/piecewise-regression/
    # my_pwlf = pwlf.PiecewiseLinFit(x, y)
    # res = my_pwlf.fit(n_clusters, disp=True)

    # Solution 3: https://github.com/DataDog/piecewise

    # manual correction of outliers, ugly, 236, 237, 558, 559, doesn't work
    start=237
    end=555
    x=x[start:end]
    y=y[start:end]
    model,all_merge_costs = pw.piecewise(x,y)
    pw.piecewise_plot(x,y,model=model)