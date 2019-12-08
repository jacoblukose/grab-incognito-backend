import csv
import pickle
import operator
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
from sklearn.metrics import confusion_matrix, classification_report 


def train_model(X, Y, model_op_path): 
	""" 
	Perform the split of data into test and train 
	Trains random forest classifier 
	Prints importances 
	Returns classifier, and split X and Y data 
	""" 
 
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=0) 
	clf = RandomForestClassifier(n_estimators=10, random_state=0, n_jobs=-1) 
	clf.fit(X_train, y_train) 

	save_model_to_disk(clf, model_op_path)
	feat_labels = X.columns 
	importances = list(zip(feat_labels, clf.feature_importances_)) 
	importances.sort(reverse=True, key=lambda x: x[1]) 
 
	print("\n Feature importances in decreasing order:") 
	print(importances) 
	return clf, X_train, X_test, y_train, y_test 

def start_train(training_data_frame, model_op_path):
	df = training_data_frame
	Y = list(df["buckets"])

	#drop Y from X
	X = df.drop(["buckets"], axis=1) 

	clf, X_train, X_test, y_train, y_test = train_model(X, Y, model_op_path) 
	print("\n == Training completed ==") 

	y_pred = clf.predict(X_test) 
	print("Y test:", y_test) 
	print("Y pred:", list(y_pred)) 
	print_confusion_matrix(y_test, y_pred)


def print_confusion_matrix(y_test, y_pred):
	"""
	print confusion matrix
	"""
	print("=== Confusion Matrix ===") 
	cm = confusion_matrix(y_test, y_pred)
	print(cm)
	plot_confusion_matrix(cm, ["NE", "E1", "E2", "E3"], normalize=True)
	plt.show()
	print('\n') 
	print("=== Classification Report ===") 
	print(classification_report(y_test, y_pred)) 
	print('\n') 


def save_model_to_disk(model, model_op_path):
	"""
	save the model to disk
	"""
	pickle.dump(model, open(model_op_path, 'wb'))

def load_model_from_disk(load_model_path):
	"""
	load the model from disk
	"""
	loaded_model = pickle.load(open(load_model_path, 'rb'))
	return loaded_model

def run_inference(input_data, load_model_path):
	"""
	Run Model inference
	"""
	model  = load_model_from_disk(load_model_path)
	result = model.predict(input_data)
	print(result)
	return result


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()


# start_train()
# run_inference()