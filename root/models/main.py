import csv
import pickle
import numpy as np
import pandas as pd
# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
from sklearn.metrics import confusion_matrix, classification_report 



def read_data(f):
	"""
	Read input data for training
	"""
	df = pd.read_csv(f)
	print(df)
	return df

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
 
	print("Feature importances in decreasing order:") 
	print(importances) 
	return clf, X_train, X_test, y_train, y_test 

def start_train(training_data_path, model_op_path):
	df = read_data(training_data_path)
	Y = list(df["buckets"])
	X = df.drop(["buckets"], axis=1) 

	clf, X_train, X_test, y_train, y_test = train_model(X, Y, model_op_path) 
	print("== Training completed ==") 

	y_pred = clf.predict(X_test) 
	print("Y test:", y_test) 
	print("Y pred:", list(y_pred)) 
	# print_confusion_matrix(y_test, y_pred)


def print_confusion_matrix(y_test, y_pred):
	"""
	print confusion matrix
	"""
	print("=== Confusion Matrix ===") 
	print(confusion_matrix(y_test, y_pred)) 
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

# start_train()
# run_inference()