from abc import ABC, abstractmethod


class Experiment(ABC):

	"""
	experiment class is the base class for all experiments.
	"""

	def __init__(self):
		pass

	@staticmethod
	@abstractmethod
	def run():
		"""
		Runs the experiment and returns the results.
		:return: results of the experiment
		"""
		pass

	@staticmethod
	@abstractmethod
	def pre_setup(self):
		"""
		Pre-setup for the experiment.
		"""
		pass

	@staticmethod
	@abstractmethod
	def post_process(self):
		"""
		Post-process for the experiment.
		"""
		pass
