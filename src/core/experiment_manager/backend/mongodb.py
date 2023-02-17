import pymongo
from .base import Backend
from config import settings

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
			raise Exception("Please connect to MongoDB before saving experiment results")

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