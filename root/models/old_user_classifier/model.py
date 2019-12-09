import pandas as pd
from root.models.main import start_train
from root.models.main import run_inference

training_data_input_path = 'dummy.csv'
model_save_path = 'old_user_classifier_model.sav'

def read_data(f):
	"""
	Read input data for training
	"""
	df = pd.read_csv(f)
	print(df)
	return df

def model_train():
	df = read_data(training_data_input_path)
	start_train(df, model_save_path)


def run_model_inference():
	input_data = [[12.9729803, 77.6295003, 1124.8, 2500, 10]]
	run_inference(input_data, model_save_path)


# model_train()
# run_model_inference()