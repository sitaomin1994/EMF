from abc import ABC, abstractmethod


# create an abc class for the experiment module
class BaseExperimentModule(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def run(self):
		pass



	