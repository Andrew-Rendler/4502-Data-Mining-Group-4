import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors              import KNeighborsClassifier
from sklearn.discriminant_analysis  import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.metrics  import confusion_matrix
from Group4_SelectProcessOrganize import *

if __name__ == '__main__':
                    #defining local variables, isolating explanatory variables from response
    feature_count = 8
    preprocessed = run_data_job()
    test_partition = 0.4
    X = preprocessed[:, :feature_count]
    y = preprocessed[:, feature_count]
                    #Show us what were working with
    print("Size of Feature Data : ",X.shape)
    print("Size of Label Data : ",y.shape)
                    #Generate random test and train sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_partition)
                    #a couple model types we experimented with
    default_model = KNeighborsClassifier(n_neighbors = 2)
    LDA_model = LinearDiscriminantAnalysis()
    LR_model = LogisticRegression()
                    #fit the default model with the training set and generate predictions for the test set
    default_model.fit(X_train, y_train)
    y_modeled = default_model.predict(X_test)
                    #evaluate the model
    delta = abs(y_modeled - y_test)
    error_count = np.count_nonzero(delta)
    print("Classifier Accuracy:",1-(error_count/len(y_test)))
    print("Average Absolute Error", np.mean(delta))
    print(confusion_matrix(y_test, y_modeled))
    
    
