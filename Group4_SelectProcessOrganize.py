import os
import pickle
import numpy as np

class subject_data:
    
    def __init__(self, path, subject):
        
        os.chdir(path)
        os.chdir(subject)
        
        self.keys = ['label', 'subject', 'signal']
        self.signals = ['wrist', 'chest']
        
        with open(subject + '.pkl', 'rb') as file:
            data = pickle.load(file, encoding='latin1')
        self.data = data

    def get_response(self):
        
        return self.data[self.keys[0]]

    def get_sensor_data(self):
        
        signal = self.data[self.keys[2]]
        return signal[self.signals[1]]

def reduce(input_data):
                    #Defining local variables and initializing arrays
    cursor = 0
    second = 700
    reduce_step = 0
    mean_features = np.empty(int(len(input_data)/second), dtype=np.double)
    std_features = np.empty(int(len(input_data)/second), dtype=np.double)  
                    #Until the cursor has stepped greater than the size of the input
    while cursor < len(input_data):
                    #Grab the next chunk of the input
        chunk = input_data[cursor:cursor+second]
                    #As long as we haven't stepped past the max possible iterations
        if reduce_step < int(len(input_data)/second):
                    #Reduce 700:1 w. mean and stdev ***mean reduced noise and stdev shows the streaming data's volatility 
            mean_features[reduce_step] = np.mean(chunk)
            std_features[reduce_step] = np.std(chunk)
                    #increment the reference points
        reduce_step = reduce_step + 1
        cursor = cursor + second
                    #consolidate arrays
    return np.column_stack((mean_features, std_features))

def isolated_features(input_data, array, state):
                    #These are the key features identified during EDA, we ingest the raw data, carve out individual sensor columns, and reduce
    ecg_features = reduce(input_data["ECG"][array].flatten())
    eda_features = reduce(input_data["EDA"][array].flatten())
    emg_features = reduce(input_data["EMG"][array].flatten())
    temp_features = reduce(input_data["Temp"][array].flatten())
                    #Consolidate arrays, tack on response
    return np.column_stack((np.hstack((eda_features, temp_features, ecg_features, emg_features)), np.full(len(np.hstack((eda_features, temp_features, ecg_features, emg_features))), state)))


def run_data_job():
                    #define local variables
    step = 0
    sID = ''
    subject_list = [2, 3, 4]
                    #for each subject, load their raw data, isolate response, isolate sensor data
    for n in subject_list:
                    
        raw_data = {}
        response_data = {}
        stacked = {}
        
        sID = 'S' + str(n)
        print("Starting Data Job for Subject ",sID)
        raw_data[sID] = subject_data("/WESAD", sID)
        response_data[sID] = raw_data[sID].get_response()
        sensor_data = raw_data[sID].get_sensor_data()
                    #initialize arrays to organize data by state
        state1_array = np.asarray([n for n, state in enumerate(response_data[sID]) if state == 1])
        state2_array = np.asarray([n for n, state in enumerate(response_data[sID]) if state == 2])
        state3_array = np.asarray([n for n, state in enumerate(response_data[sID]) if state == 3])
                    #isolate and reduce features, stack or union the sets
        stacked[sID] = np.vstack((isolated_features(sensor_data, state1_array, 1), isolated_features(sensor_data, state2_array, 2), isolated_features(sensor_data, state3_array, 3)))
        print("Completed Data Job for Subject ",sID,". Shape: ",stacked[sID].shape)
    
    for n, m in stacked.items():
                    #now unwind that data into something usable
        if step == 0:
            
            data = stacked[n]
            step = step + 1
            
        data = np.vstack((data, stacked[n]))
                    #and send it on back!
    return data

if __name__ == '__main__':
    
    run_data_job()
    print("Data Job Complete")

