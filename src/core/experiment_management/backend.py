from abc import ABC, abstractmethod
import pymongo
import json
from pathlib import Path
from config import settings, ROOT_DIR
import base64


class Backend(ABC):

	def __init__(self):
		pass

	@abstractmethod
	def connect(self):
		pass

	@abstractmethod
	def save(self, experiment_name, experiment_result):
		pass


class MongoBackend(Backend):

	def __init__(self):
		super().__init__()
		self.client = None
		self.db = None
		self.collection = None
		self.db_name = settings['mongodb_backend']['db']

	def connect(self):
		self.client = pymongo.MongoClient("mongodb://localhost:27017/")
		self.db = self.client[self.db_name]

	def save(self, experiment_type, experiment_result):
		if self.db is None:
			raise Exception("Please connect to MongoDB before saving experiment_tmpl results")

		if experiment_type not in self.db.list_collection_names():
			self.db.create_collection(experiment_type)

		collection = self.db[experiment_type]
		collection.insert_one(experiment_result)

	def find_experiments(self, experiment_type, query):
		if self.db is None:
			raise Exception("Please connect to MongoDB before finding experiments")

		if experiment_type not in self.db.collection_names():
			raise Exception("Experiment type {} not found in database".format(experiment_type))

		collection = self.db[experiment_type]
		return collection.find(query)

	def disconnect(self):
		self.client.close()


class FileBackend:

	def __init__(self):
		self.result_dir_path = settings['experiment_result_dir']
		self.config_dir_path = settings['experiment_config_dir']

	def save(self, dir_name, file_name, experiment_data):
		# create directory if not exists
		dir_path = ROOT_DIR + "/" + self.result_dir_path + '/' + dir_name
		Path(dir_path).mkdir(parents=True, exist_ok=True)

		# save experiment_tmpl data
		with open(dir_path + '/' + file_name, 'w') as f:
			json.dump(experiment_data, f)

		if "results" in experiment_data:
			img_file_name = file_name.replace(".json", '.png')
			if "plots" in experiment_data["results"]:
				with open(dir_path + '/' + img_file_name, 'wb') as f:
					f.write(base64.b64decode(experiment_data["results"]["plots"][0]))
