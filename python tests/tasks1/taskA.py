class TaskA(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('a')
		self.inputs.declare('b')
		self.outputs.declare('c')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.c = self.a + self.
