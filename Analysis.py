import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Data import SubjectData


if __name__ == '__main__':
    
    newSubject = SubjectData(11)
    data = newSubject.getData('EMG')
    newSubject.graphData('EMG')
