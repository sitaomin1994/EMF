from abc import ABC, abstractmethod


class Backend(ABC):

	def __init__(self):
		pass

	@abstractmethod
	def connect(self):
		pass

	@abstractmethod
	def save(self, experiment_name, experiment_result):
		pass