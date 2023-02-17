

class Experiment:

	"""
	experiment class is the base class for all experiments.
	"""

	def __init__(self, experiment_modules: list):
		self.experiment_modules = experiment_modules

	def run(self):
		"""
		Runs the experiment and returns the results.
		:return: results of the experiment
		"""
		pass
