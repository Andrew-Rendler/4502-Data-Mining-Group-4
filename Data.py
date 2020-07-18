import os
import pickle
import numpy as np
import pandas as pd

#credit to github user WJMatthew
class SubjectData:

    def __init__(self, subject_number):

        self.subject = f'S{subject_number}'

        #this assumes WESAD has same depth as project root
        with open(os.path.join('../', self.subject) + '/' + self.subject + '.pkl', 'rb') as file:
            self.data = pickle.load(file, encoding='latin1')
        self.chestData = self.data['signal']['chest']
        self.wristData = self.data['signal']['wrist']
        self.labels = self.data['label']

    def getData(self,key):
        if key not in ['ACC', 'ECG', 'EMG', 'EDA', 'Temp', 'Resp']:
            print('Key not found, select from ACC, ECG, EMG, EDA, Temp, Resp')
        else: return self.chestData['signal']['wrist'][f'{key}']


    def graphData(self,key):
        if key not in ['ACC', 'ECG', 'EMG', 'EDA', 'Temp', 'Resp']:
            print('Key not found, select from ACC, ECG, EMG, EDA, Temp, Resp')
        else:

            plt.plot(self.chestData['signal']['wrist'][f'{key}'],'bo')
            plt.show()
