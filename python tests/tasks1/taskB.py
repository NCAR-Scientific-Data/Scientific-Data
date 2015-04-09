class TaskB(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('d')
		self.outputs.declare('e')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.e = self.d*3