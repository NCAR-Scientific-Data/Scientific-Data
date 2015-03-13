import pyutilib.workflow

class TaskA(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('a')
		self.inputs.declare('b')
		self.outputs.declare('c')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.c = self.a + self.b

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
		self.outputs.declare('g')
		self.outputs.declare('h')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.f = self.e*self.c
		self.g = self.f/2
		self.h = self.f/4

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

class TaskG(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('j')
		self.inputs.declare('k')
		self.inputs.declare('l')
		self.outputs.declare('m')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.m = self.j+self.k+self.l

def run():
	A = TaskA()
	B = TaskB()
	C = TaskC()
	D = TaskD()
	D2 = TaskD()
	E = TaskE()
	G = TaskG()
	w = pyutilib.workflow.Workflow()
	A.inputs.a = 1
	A.inputs.b = 2
	B.inputs.d = 3
	D2.inputs.g = 4
	C.inputs.e = A.outputs.c
	C.inputs.c = B.outputs.e
	E.inputs.h = C.outputs.h
	E.inputs.f = C.outputs.f
	D.inputs.g = C.outputs.g
	G.inputs.j = D.outputs.h
	G.inputs.k = E.outputs.i
	G.inputs.l = D2.outputs.h
	w.add(A)
	w.add(B)
	w.add(C)
	w.add(D)
	w.add(D2)
	w.add(E)
	w.add(G)

	l = w.__list__()
	return { "workflow": l}
