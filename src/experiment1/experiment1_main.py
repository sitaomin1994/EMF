from ..core.Experiment import Experiment


class Experiment1(Experiment):

	def __init__(self):
		super().__init__()

	def run(self):
		print("Experiment1.run()")

	def pre_setup(self):
		print("Experiment1.pre_setup()")

	def post_process(self):
		print("Experiment1.post_process()")