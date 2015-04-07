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

class TaskB(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('d')
		self.outputs.declare('e')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.e = self.d*3

class TaskC(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('e')
		self.inputs.declare('c')
		self.outputs.declare('f')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.f = self.e*self.c

class TaskD(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('g')
		self.outputs.declare('h')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.h = self.g*self.g

class TaskE(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('h')
		self.inputs.declare('f')
		self.outputs.declare('i')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.i = self.h+self.f

class TaskF(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('hi')
		self.outputs.declare('h')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.h = self.g*self.g