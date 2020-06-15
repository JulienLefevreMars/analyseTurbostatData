import numpy as np
from sklearn.metrics import mutual_info_score

def averaging(signal,nstep):
    """
    Signal averaging
    :param signal: array (n,), n steps
    :param nstep: nstep is the length of the window on which the signal is averaged
    :return: (n/nstep,) array
    """
    n=signal.shape[0]
    end=n//nstep
    averaged_signal=np.mean(np.reshape(signal[:end*nstep],(end,nstep)),axis=1)
    return averaged_signal

def mutual_information(signal1,signal2,nbins1=None,nbins2=None):
    if nbins1==None:
        nbins1=np.sqrt(len(signal1))
    if nbins2==None:
        nbins2=np.sqrt(len(signal2))
    H=np.histogram2d(signal1,signal2,bins=[nbins1,nbins2])
    # TO BE CONTINUED

def register(signal1,signal2,t1=None,t2=None,similarity=np.corrcoef):
    """
    Register two temporal series, assumed to have the same sampling
    :param signal1: first temporal serie
    :param signal2: second temporal serie
    :param t1: left boundary of the possible shift intervals
    :param t2: right boundary of the possible shift intervals
    :param similarity: similarity metric between two arrays
    :return: the temporal shift that maximizes a similarity metric
    """

    n1=len(signal1)
    n2=len(signal2)
    if n1>n2:
        (signal1,signal2)=(signal2,signal1)

    if (t1==None):
        t1=-n1//10
        t2=-t1
    correlations=np.zeros((t2-t1,))
    for i,t in enumerate(range(t1,t2)):
        if t<0:
            C=similarity(signal1[-t:],signal2[0:n1+t])
        if t>=0:
            C=similarity(signal1[0:min(n2-t,n1)],signal2[t:t+min(n2-t,n1)])
        correlations[i]=C[0,1]

    return correlations