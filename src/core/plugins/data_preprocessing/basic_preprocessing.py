import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


########################################################################################################################
# Normalization
########################################################################################################################
def normalization(data, target_col, type='minmax'):

	data_X = data.drop([target_col], axis=1).values
	if type == 'minmax':
		scaler = MinMaxScaler()
	elif type == 'standard':
		scaler = StandardScaler()
	else:
		raise ValueError("Normalization type not supported")

	new_data_X = scaler.fit_transform(data_X)
	data.loc[:, data.columns != target_col] = new_data_X

	return data


########################################################################################################################
# Ordering columns
########################################################################################################################
def move_target_to_end(data, target_col):
	"""
	Move the target column to the end of the data
	:param data: original data
	:param target_col: target column
	:return: reordered data
	"""
	target_col_series = data[target_col]
	data = data.drop(target_col, axis=1)
	data.insert(len(data.columns), target_col, target_col_series)

	return data


def reorder_data(data: pd.DataFrame, num_cols: list, cat_cols: list, target_cols: list, sensitive_cols: list = None):
	"""
	Reorder the data columns to be in the order of num_cols, cat_cols, sensitive_cols, target_cols
	:param data: original data
	:param num_cols: numerical columns
	:param cat_cols: categorical columns
	:param target_cols: target columns
	:param sensitive_cols: sensitive columns
	:return: reordered data
	"""
	if sensitive_cols is None:
		sensitive_cols = []

	if target_cols is None:
		target_cols = []

	ret_columns = num_cols + cat_cols + sensitive_cols + target_cols
	data = data[ret_columns]

	return data


