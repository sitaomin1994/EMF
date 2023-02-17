from .backend import MongoBackend, FileBackend
from .utils import generate_experiment_file_name, consolidate_experiment_data
from loguru import logger
import time as time


class ExperimentManager:

	def __init__(self, db_backend_option='mongodb'):
		# db backend
		if db_backend_option == 'mongodb':
			self.backend = MongoBackend()
		else:
			raise NotImplementedError
		# file backend
		self.file_backend = FileBackend()

		# experiment instance
		self.experiment_class = None

	def set_experiment(self, experiment_class):
		self.experiment_class = experiment_class

	def run_experiments(self, configuration_files, experiment_type, experiment_meta=None, labels:list=None):

		# connect to backend database
		self.backend.connect()
		logger.info("Connected to backend database")

		# save experiment meta data
		if experiment_meta is not None:
			self.file_backend.save(experiment_type, '', experiment_meta["filename"], experiment_meta)
			self.backend.save(experiment_type, experiment_meta)
			logger.info("Saved experiment meta data")
		labels_info = labels.pop()

		# experiment start
		logger.info("Running {} experiments".format(len(configuration_files)))
		start_global = time.time()

		# run experiments
		for idx, config in enumerate(configuration_files):
			print("=" * 200)
			logger.info("Experiment - {}".format(idx))
			start = time.time()

			############################################################
			# Experiment main process
			logger.info("config: {}".format(config))
			logger.info("labels: {}".format(labels[idx]))
			experiment = self.experiment_class()
			ret = experiment.run_experiment(config)

			#############################################################
			end = time.time()
			logger.info("Experiment finished in {}".format(end - start))

			# save results to backend
			dir_name, file_name = generate_experiment_file_name(labels[idx], labels_info)
			running_stats = {
				'time': time.time(),
				'elapsed_time': end - start,
				'file_path': dir_name + '/' + file_name
			}
			experiment_data = consolidate_experiment_data(experiment_type, config, ret, running_stats)
			self.file_backend.save(experiment_type, dir_name, file_name, experiment_data)
			self.backend.save(experiment_type, experiment_data)
			logger.info("Experiment saved to backend database")

		# total time and summary
		end_global = time.time()
		logger.info("Total time: {}".format(end_global - start_global))

		# disconnect from backend database
		self.backend.disconnect()
		logger.info("Disconnected from backend database")
