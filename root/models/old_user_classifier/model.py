from root.models.main import start_train
from root.models.main import run_inference

training_data_input_path = 'dummy.data'
model_save_path = 'old_user_classifier_model.sav'


def model_train():
	start_train(training_data_input_path, model_save_path)


def run_model_inference():
	input_data = [[12.9729803, 77.6295003, 1124.8, 2500, 10]]
	run_inference(input_data, model_save_path)


# model_train()
run_model_inference()