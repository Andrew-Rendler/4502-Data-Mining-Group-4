import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#credit to github user WJMatthew
class SubjectData:

    def __init__(self, subject_number):

        self.subject = f'S{subject_number}'

        #this assumes WESAD has same depth as project root
        with open(os.path.join('../WESAD', self.subject) + '/' + self.subject + '.pkl', 'rb') as file:
            self.data = pickle.load(file, encoding='latin1')
        self.chestData = self.data['signal']['chest']
        self.wristData = self.data['signal']['wrist']
        self.labels = self.data['label']

    def getData(self,key):
        if key not in ['ACC', 'ECG', 'EMG', 'EDA', 'Temp', 'Resp']:
            print('Key not found, select from ACC, ECG, EMG, EDA, Temp, Resp')
        else: return self.chestData[f'{key}']


    def graphLabelData1D(self):

        ms = []
        for i in range(0,len(self.labels)):
            ms.append((i/700)*1000) #conversion to MIlliseconds

        plt.plot(ms,self.labels,'r')
        plt.ylabel('Label')
        plt.grid(True)
        plt.show()


    def graphSignalData1D(self, key, xLabel, yLabel, Overlay = False):
        if key not in ['ACC', 'ECG', 'EMG', 'EDA', 'Temp', 'Resp']:
            print('Key not found, select from ACC, ECG, EMG, EDA, Temp, Resp')
        else:
            ms = []
            for i in range(0,len(self.chestData[f'{key}'])):
                ms.append((i/700)*1000) #conversion to MIlliseconds

            plt.plot(ms,self.chestData[f'{key}'])
            plt.xlabel(xLabel)
            plt.ylabel(yLabel)

            if Overlay:
                plt.plot(range(0,len(self.labels)),self.labels,'ro')
            plt.show()

    def graphData2D(self,key):
        pass

    def graphSignalData1DSmoothed(self, key, factor, xLabel, yLabel, Overlay = False):
        if key not in ['ACC', 'ECG', 'EMG', 'EDA', 'Temp', 'Resp']:
            print('Key not found, select from ACC, ECG, EMG, EDA, Temp, Resp')
        else:
            data = self.chestData[f'{key}']
            smoothed = np.mean(data.reshape(-1, factor), axis=1)
            ms = range(0,len(data),factor)

            print(len(smoothed))

            plt.plot(ms,smoothed)
            plt.xlabel(xLabel)
            plt.ylabel(yLabel)

            if Overlay:
                plt.plot(range(0,len(self.labels)),self.labels,'ro')

            plt.show()
