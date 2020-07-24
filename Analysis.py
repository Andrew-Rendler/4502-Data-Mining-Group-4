import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Data import SubjectData

units = {'ACC':'1/64g', 'ECG':'mV', 'EMG':'mV', 'EDA':'μS', 'Temp':'°C', 'Resp':'%'}
#Length of all arrays 3663100
#sampling at 700Hz (1/700s interval)

if __name__ == '__main__':

    newSubject = SubjectData(14)
    #print(newSubject.data.keys())
    print(newSubject.data['label'])

    attribute = 'EDA'
    newSubject.graphSignalData1DSmoothed(attribute,100,'Milliseconds',units[attribute])
    #newSubject.graphLabelData1D()
