import pandas as pd


def loading_data(data_path):

	df = pd.read_csv(data_path)

	return df

