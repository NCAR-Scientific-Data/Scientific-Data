from tasks1 import TaskA
from tasks1 import TaskB
from tasks1 import TaskD

def getInstance(taskType):
	if taskType == 'TaskA':
		return TaskA()
	if taskType == 'TaskB':
		return TaskB()
	if taskType == 'TaskD':
		return TaskD()