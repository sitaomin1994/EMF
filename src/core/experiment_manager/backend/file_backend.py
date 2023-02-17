import json
from pathlib import Path
from config import settings, ROOT_DIR
import base64

class FileBackend:

	def __init__(self):
		self.result_dir_path = settings['experiment_result_dir']
		self.config_dir_path = settings['experiment_config_dir']

	def save(self, experiment_type, dir_name, file_name, experiment_data):
		# create directory if not exists
		dir_path = ROOT_DIR + "/" + self.result_dir_path + '/' + experiment_type + '/' + dir_name
		Path(dir_path).mkdir(parents=True, exist_ok=True)

		# save experiment data
		with open(dir_path + '/' + file_name, 'w') as f:
			json.dump(experiment_data, f)

		if "results" in experiment_data:
			img_file_name = file_name.replace(".json", '.png')
			with open(dir_path + '/' + img_file_name, 'wb') as f:
				f.write(base64.b64decode(experiment_data["results"]["plots"][0]))