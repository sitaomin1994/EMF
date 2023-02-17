from datetime import datetime


def consolidate_experiment_data(experiment_type, configuration, results, running_stats):

	experiment_data = dict()

	# meta data
	experiment_data['type'] = "experiment_data"
	experiment_data['experiment_type'] = experiment_type
	experiment_data['file_path'] = running_stats['file_path']
	experiment_data['timestamp'] = running_stats['time']
	experiment_data['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	experiment_data['running_time'] = running_stats['elapsed_time']
	experiment_data['status'] = 'finished'

	# parameters, results
	experiment_data["params"] = configuration
	experiment_data["results"] = results

	return experiment_data


def generate_experiment_file_name(labels, labels_info):

	dirs, fields = [], []
	for label, label_info in zip(labels, labels_info):
		if label_info[1] == 'dir':
			dirs.append(label)
		else:
			fields.append(label_info[0] + '_' + str(label))

	dir_name = '/'.join(dirs)
	file_name = "@".join(fields) + ".json"

	return dir_name, file_name
