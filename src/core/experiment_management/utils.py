from datetime import datetime
import dataclasses

def consolidate_experiment_data(configuration, results, exp_stats):

	experiment_data = dict()

	# meta data
	experiment_data['type'] = "experiment_data"
	experiment_data['experiment_type_id'] = exp_stats['exp_id']
	experiment_data['experiment_type'] = exp_stats['exp_name']
	experiment_data['file_path'] = exp_stats['file_path']
	experiment_data['timestamp'] = exp_stats['time']
	experiment_data['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	experiment_data['running_time'] = exp_stats['elapsed_time']
	experiment_data['status'] = 'finished'

	# parameters, results
	experiment_data["params"] = dataclasses.asdict(configuration)
	experiment_data["results"] = results

	return experiment_data
