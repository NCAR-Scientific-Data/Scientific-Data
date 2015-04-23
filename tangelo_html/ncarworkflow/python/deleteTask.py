import test
import pyutilib.workflow
import uuid
import json
import re


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
	def execute(self):
		"""Compute the sum of the inputs."""
		self.f = self.e*self.c

# Add task with linkks to workflow
def addTask(task, taskUID, links, workflow):
	for i in task.inputs:
		# Input is Port
		# links = ['Port', UID,] 
		if(links[i][0] == 'Port'):
			# Do not add link to deleted task with UID = taskUID
			if(not taskUID == links[i][1]):
				# Find the task in the workflow with UID in link[i]
				t = workflow._dfs_([workflow._start_task.id], lambda t: t.getTaskWithID(links[i][1]))[0]
				# Reset the tasks outputs
				t.reset_all_outputs()
				# Set the input to the outputs of found task

				task.inputs[i] = t.outputs[links[i][2]]
			else:
				task.inputs[i] = None
		# Input is number
		# TODO:
		# Better checking
		else:
			task.inputs[i] = links[i][0]

	# Add updated task to workflow and return new workflow
	workflow.add(task)
	return workflow

# Build a workflow from json file with id workflowID
# Do not add task with UID = taskUID
def deserialize(taskUID, workflowID):
	with open('data/'+workflowID+'.json') as data_file:    
		data = json.load(data_file)
	# Create temp workflow
	q = pyutilib.workflow.Workflow()
	for task in data:
		# Dont recreate empty tasks (done for you)
		if (task['Type'] not in ['EmptyTask']) and (task['UID'] not in [taskUID]):
			# Create instance of specified task
			# TODO:
			# Make this a factory and replace with actual tasks
			t = test.getInstance(task['Type'])
			# Set UID to its previous instance's
			# This is so the particular task in the workflow
			# will always be linked properly
			t.setUID(task['UID'])
			t.setWorkflowID(task['WorkflowID'])
			# Add task t to workflow q with proper inputs
			addTask(t, taskUID, task['Inputs'], q)
	return q

# Serialize workflow into json file with UID as filename
def serialize(workflow):
	with open('data/'+workflow.workflowID+'.json', 'w') as outfile:
		print(workflow.__dict__())
		json.dump(workflow.__dict__(), outfile)


def run(taskUID, workflowUID):
	# Build workflow with filename workflowUID.json
	# Don't add task with UID = taskUID
	workflow = deserialize(taskUID, workflowUID)
	workflow.setWorkflowID(workflowUID)
	serialize(workflow)

w = pyutilib.workflow.Workflow()
w.setWorkflowID(str(uuid.uuid4()))


A = TaskA()
A.setUID(str(uuid.uuid4()))
A.setWorkflowID(w.workflowID)
B = TaskB()
B.setUID(str(uuid.uuid4()))
B.setWorkflowID(w.workflowID)
C = TaskC()
C.setUID(str(uuid.uuid4()))
C.setWorkflowID(w.workflowID)
A.inputs.a = 1
A.inputs.b = 2
B.inputs.d = A.outputs.c
C.inputs.e = B.outputs.e
C.inputs.c = 2
w.add(A)
w.add(B)
w.add(C)
serialize(w)


run(B.uid, w.workflowID)