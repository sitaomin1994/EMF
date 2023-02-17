import pandas as pd
from sklearn.model_selection import KFold


########################################################################################################################
# Split dataset into n folds
########################################################################################################################
def split_train_test(dataset: pd.DataFrame, n_folds=5, seed=0):
	"""
	Split dataset into n folds train and test sets
	:param dataset: pandas dataset to split
	:param n_folds: number of folds
	:param seed: random seed
	:return: list of train and test sets
	"""
	# split into n folds
	k_fold = KFold(n_folds, random_state=seed, shuffle=True)
	splits = k_fold.split(dataset)

	# split into train and test sets
	train_test_sets = []
	for train_index, test_index in splits:
		train_set = dataset.iloc[train_index]
		test_set = dataset.iloc[test_index]
		train_test_sets.append((train_set, test_set))

	return train_test_sets

