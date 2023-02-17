import pandas as pd


# binning numerical features
def binning(data, target_col, bins=10, type='equal_width'):
	data_X = data.drop([target_col], axis=1).values
	if type == 'equal_width':
		data_X = pd.cut(data_X, bins=bins, labels=False)
	elif type == 'equal_freq':
		data_X = pd.qcut(data_X, q=bins, labels=False)
	else:
		raise ValueError("Binning type not supported")

	data.loc[:, data.columns != target_col] = data_X

	return data
