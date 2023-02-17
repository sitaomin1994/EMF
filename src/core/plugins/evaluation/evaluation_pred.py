from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def eval_clf(y_true, y_pred):
	return {
		"accuracy": accuracy_score(y_true, y_pred),
		"precision": precision_score(y_true, y_pred),
		"recall": recall_score(y_true, y_pred),
		"f1": f1_score(y_true, y_pred),
		"roc_auc": roc_auc_score(y_true, y_pred)
	}


def eval_reg(y_true, y_pred):
	return {
		"mse": mean_squared_error(y_true, y_pred),
		"mae": mean_absolute_error(y_true, y_pred),
		"r2": r2_score(y_true, y_pred)
	}