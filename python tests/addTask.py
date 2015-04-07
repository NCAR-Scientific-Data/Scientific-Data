from test import TaskA
from test import TaskB
import pyutilib.workflow
import uuid
import json

def get_Task(taskType):
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

def addTask(task, links, workflow):
	for i in task.inputs:
		# PROBLEM HERE
		if(type(links[i][0]) == pyutilib.workflow.port.Port):
			links[i][1].reset_all_outputs()
			task.inputs[i] = links[i][0]
		else:
			task.inputs[i] = links[i][0]

	workflow.add(task)
	return workflow

def deserialize(workflowID):
	with open(workflowID+'.json') as data_file:    
		data = json.load(data_file)

	q = pyutilib.workflow.Workflow()
	for task in data:
		if not task['Type'] in ['EmptyTask']:
			t = get_Task(task['Type'])
			addTask(t, task['Inputs'], q)
	return q

def serialize(workflow):
	with open(workflow.workflowID+'.json', 'w') as outfile:
		json.dump(workflow.__dict__(), outfile)

def run(task, links, workflowID):
	workflow = deserialize(workflowID)
	workflow = addTask(task, links, workflow)

	workflow.setWorkflowID(workflowID)
	serialize(workflow)

	output = workflow()
	result = [int(s) for s in output.__str__().split() if s.isdigit()]
	return {"result":result, "list":workflow.__list__()}

w = pyutilib.workflow.Workflow()
w.setWorkflowID(str(uuid.uuid4()))
serialize(w)
A = TaskA()
B = TaskB()
test = run(A, {"a" :[21], "b":[4]}, w.workflowID)
test1 = run(B, {"d": [A.outputs.c, A]}, w.workflowID)
