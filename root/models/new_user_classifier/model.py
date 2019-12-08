import pandas as pd
from root.models.main import start_train
from root.models.main import run_inference
from sklearn import preprocessing

training_data_input_path = 'dummy.csv'
model_save_path = 'new_user_classifier_model.sav'

def preprocess_data(df):

	#perform one hotting for categorical values
	
	# 1. INSTANTIATE
	# encode labels with value between 0 and n_classes-1.
	le = preprocessing.LabelEncoder()
	#select all categorical
	X_categorical = df.select_dtypes(include=[object])
	#select all non categorical
	X_others = df.select_dtypes(exclude=[object])

	# 2/3. FIT AND TRANSFORM
	# use df.apply() to apply le.fit_transform to all columns	
	X_2 = X_categorical.apply(le.fit_transform)

	#join column wise both	
	final_df = X_2.join(X_others)
	return final_df
	
def read_data(f):
	"""
	Read input data for training
	"""
	df = pd.read_csv(f)
	return df

def model_train():
	df = read_data(training_data_input_path)
	
	#we dont want to preprocess Y
	Y = df['buckets']
	df = df.drop(["buckets"], axis=1) 
	# print(df)
	preprocessed_df = preprocess_data(df)
	
	#Add Y back
	preprocessed_df['buckets'] = Y
	print(preprocessed_df)
	start_train(preprocessed_df, model_save_path)


def run_model_inference():
	input_data = [[22,12.9729803,77.6295003,'M','N','software intern']]
	dfObj = pd.DataFrame(input_data)
	#perform one hotting for input data
	input_preprocessed = preprocess_data(dfObj)
	# print(input_preprocessed)
	run_inference(input_preprocessed, model_save_path)



model_train()
# run_model_inference()