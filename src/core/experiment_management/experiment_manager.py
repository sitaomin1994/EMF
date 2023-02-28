from .backend import MongoBackend, FileBackend
from .utils import consolidate_experiment_data
from loguru import logger
import time as time
import multiprocessing as mp


class ExperimentManager:

	def __init__(self, db_backend_option='mongodb'):
		# db backend
		if db_backend_option == 'mongodb':
			self.backend = MongoBackend()
		else:
			raise NotImplementedError
		# file backend
		self.file_backend = FileBackend()

		# experiment1 instance
		self.experiment_class = None

	def set_experiment(self, experiment_class):
		self.experiment_class = experiment_class

	def run_experiments(
			self, exp_configs, experiment_meta, use_db=False
	):
		experiment_type = experiment_meta['exp_name']
		experiment_id = experiment_meta['exp_id']
		if use_db:
			# connect to backend database
			self.backend.connect()
			logger.info("Connected to backend database")

			# save experiment1 meta data
			self.backend.save(experiment_type, experiment_meta)
			logger.info("Saved experiment1 meta data")
		else:
			self.file_backend.save(
				experiment_meta["dir_name"], experiment_meta["filename"], experiment_meta
			)
			logger.info("Saved experiment1 meta data")

		# experiment1 start
		logger.info("Running {} experiments".format(len(exp_configs)))
		start_global = time.time()

		# run experiments
		for idx, exp_config in enumerate(exp_configs):
			print("=" * 200)
			logger.info("Experiment - {}".format(idx))
			logger.info("Experiment - {}".format(exp_config.keys))
			logger.info("Experiment - {}".format(exp_config.values))
			start = time.time()

			############################################################
			# Experiment main process
			# logger.info("config: {}".format(exp_config.config))
			experiment = self.experiment_class()
			ret = experiment.run_experiment(exp_config.config)

			#############################################################
			end = time.time()
			logger.info("Experiment finished in {}".format(end - start))

			# save results to backend
			dir_name, file_name = exp_config.dir_name, exp_config.file_name
			exp_stats = {
				'exp_id': experiment_id,
				'exp_name': experiment_type,
				'time': time.time(),
				'elapsed_time': end - start,
				'file_path': dir_name + '/' + file_name
			}
			experiment_data = consolidate_experiment_data(exp_config, ret, exp_stats)
			self.file_backend.save(dir_name, file_name, experiment_data)

			if use_db:
				self.backend.save(experiment_type, experiment_data)
				logger.info("Experiment saved to backend database")

		# total time and summary
		end_global = time.time()
		logger.info("Total time: {}".format(end_global - start_global))

		# disconnect from backend database
		if use_db:
			self.backend.disconnect()
		logger.info("Disconnected from backend database")

	def run_experiment_mtp(self, exp_configs, experiment_meta, use_db=False):
		experiment_type = experiment_meta['exp_name']
		experiment_id = experiment_meta['exp_id']
		if use_db:
			# connect to backend database
			self.backend.connect()
			logger.info("Connected to backend database")

			# save experiment1 meta data
			self.backend.save(experiment_type, experiment_meta)
			logger.info("Saved experiment1 meta data")
		else:
			self.file_backend.save(
				experiment_meta["dir_name"], experiment_meta["filename"], experiment_meta
			)
			logger.info("Saved experiment1 meta data")

		num_processes = 8
		chunk_size = len(exp_configs) // num_processes
		#chunks = [exp_configs[i:i + chunk_size] for i in range(0, len(exp_configs), chunk_size)]

		# experiment1 start
		logger.info("Running {} experiments parallel".format(len(exp_configs)))
		with mp.Pool(num_processes) as pool:
			process_args = [(idx, exp_config, experiment_type, experiment_id, self.experiment_class, self.file_backend,
			                 self.backend, use_db) for idx, exp_config in enumerate(exp_configs)]
			pool.starmap(self.run_chunk_experiment, process_args, chunksize=chunk_size)

		# disconnect from backend database
		if use_db:
			self.backend.disconnect()
		logger.info("Disconnected from backend database")

	@staticmethod
	def run_chunk_experiment(
			idx, exp_config, experiment_type, experiment_id, experiment_class, file_backend, backend, use_db
	):
		# run experiments
		print("=" * 200)
		logger.info("Experiment - {}".format(idx))
		logger.info("Experiment - {}".format(exp_config.keys))
		logger.info("Experiment - {}".format(exp_config.values))
		start = time.time()

		############################################################
		# Experiment main process
		# logger.info("config: {}".format(exp_config.config))
		experiment = experiment_class()
		ret = experiment.run_experiment(exp_config.config)

		#############################################################
		end = time.time()
		logger.info("Experiment finished in {}".format(end - start))

		# save results to backend
		dir_name, file_name = exp_config.dir_name, exp_config.file_name
		exp_stats = {
			'exp_id': experiment_id,
			'exp_name': experiment_type,
			'time': time.time(),
			'elapsed_time': end - start,
			'file_path': dir_name + '/' + file_name
		}
		experiment_data = consolidate_experiment_data(exp_config, ret, exp_stats)
		file_backend.save(dir_name, file_name, experiment_data)

		if use_db:
			backend.save(experiment_type, experiment_data)
			logger.info("Experiment saved to backend database")
