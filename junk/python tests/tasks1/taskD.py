class TaskD(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('g')
		self.outputs.declare('h')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.h = self.g*self.g