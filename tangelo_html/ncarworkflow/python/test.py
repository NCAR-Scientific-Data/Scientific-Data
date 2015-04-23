import pyutilib.workflow
import uuid
import json
import ast

class TaskA(pyutilib.workflow.Task):
	def __init__(self, *args, **kwds):
		"""Constructor."""
		pyutilib.workflow.Task.__init__(self, *args, **kwds)
		self.inputs.declare('a')
		self.inputs.declare('b')
		self.outputs.declare('c')
	def execute(self):
		"""Compute the sum of the inputs."""
		self.c = "test.nc"

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

def addTask(task, links, workflow):
	#temp = pyutilib.workflow.Workflow()
	for i in task.inputs:
		if(type(links[i][0]) == pyutilib.workflow.port.Port):
			links[i][1].reset_all_outputs()
			task.inputs[i] = links[i][0]
		else:
			task.inputs[i] = links[i][0]

	workflow.add(task)
	return workflow

def getInstance(taskType):
	if taskType == 'TaskA':
		return TaskA()
	if taskType == 'TaskB':
		return TaskB()
	if taskType == 'TaskC':
		return TaskC()
	if taskType == 'TaskD':
		return TaskD()
	if taskType == 'TaskE':
		return TaskE()
	if taskType == 'TaskF':
		return TaskF()


def createWorkflow():
	w = pyutilib.workflow.Workflow()
	A = TaskA()
	B = TaskB()
	A1 = TaskA()

	A.inputs.a = 1
	A.inputs.b = 2
	B.inputs.d = A.outputs.c
	A1.inputs.a = 3
	A1.inputs.b = 4
	w.add(A)
	w.add(B)
	w.add(A1)
	print(w())

createWorkflow()
