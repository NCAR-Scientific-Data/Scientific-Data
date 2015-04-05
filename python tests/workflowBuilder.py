from test import TaskA
from test import TaskB
import pyutilib.workflow

w = pyutilib.workflow.Workflow()

def addTask(task, links):
	#temp = pyutilib.workflow.Workflow()
	for i in task.inputs:
		task.inputs[i] = links[i]
	#task._set_inputs(inputs)
	# Add task to temp workflow to speed things up
	# Temp workflow only contains the running task
	#temp.add(task)
	# Run workflow and store output
	#output = temp()
	# Add task to current workflow
	global w
	w.add(task)
	output = w()
	result = [int(s) for s in output.__str__().split() if s.isdigit()]
	return [result, w]


A = TaskA()
test = addTask(A, {"a" :21, "b":4})
B = TaskB()
test1 = addTask(B, {"d": A.outputs.c})
print(test1[1].__list__())
print(w.__list__())
