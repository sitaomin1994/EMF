from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder
import numpy as np


def one_hot_encoding(data, categories=None, max_categories=10):
	if categories:
		enc = OneHotEncoder(categories=categories, handle_unknown='ignore', max_categories=max_categories)
	else:
		enc = OneHotEncoder(handle_unknown='ignore', max_categories=max_categories)
	one_hot_encoded_data = enc.fit_transform(data)
	return one_hot_encoded_data
