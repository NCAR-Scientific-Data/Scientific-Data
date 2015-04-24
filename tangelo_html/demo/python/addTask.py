import test
import pyutilib.workflow
import uuid
import json
import re

from pymongo import MongoClient


# Add task with links to workflow
def addTask(task, links, workflow):
	for i in task.inputs:
		# Input is Port
		if(links[i][0] == 'Port'):
			# Find the task in the workflow with UID in link[i]
			t = workflow._dfs_([workflow._start_task.id], lambda t: t.getTaskWithID(links[i][1]))
			# Reset the tasks outputs
			t[0].reset_all_outputs()
			# Set the input to the outputs of found task
			task.inputs[i] = t[0].outputs[links[i][2]]
		# Input is number
		# TODO:
		# Better checking
		else:
			task.inputs[i] = links[i][0]

	# Add updated task to workflow and return new workflow
	workflow.add(task)
	return workflow

# Build a workflow from json file with id workflowID
def deserialize(workflowID):
	# open mongodb client and database
	client = MongoClient()
	db = client.testdb
	collection = db.testcollection
	
	data = collection.find_one({"_id": workflowID})

	# Create temp workflow
	q = pyutilib.workflow.Workflow()
	for task in data:
		# Dont recreate empty tasks (done for you)
		if not task['Type'] in ['EmptyTask']:
			# Create instance of specified task
			# TODO:
			# Make this a factory and replace with actual tasks
			t = task.getInstance(task['Type'])
			# Set UID to its previous instance's
			# This is so the particular task in the workflow
			# will always be linked properly
			t.setUID(task['UID'])
			# Add task t to workflow q with proper inputs
			addTask(t, task['Inputs'], q) 
	return q

# Serialize workflow into json file with UID as filename
def serialize(workflow):
	with open('json/'+workflow.workflowID+'.json', 'w') as outfile:
		json.dump(workflow.__dict__(), outfile)

# Call this function to add a new task to a workflow
def run(taskType, links, workflowID, repop):
	# Build workflow with filename workflowID.json
	workflow = deserialize(workflowID)
	# Add task to the workflow
	# TODO:
	# MAKE the task input be a type and call a factory to get instance of task
	task = test.getInstance(taskType)
	task.setUID(str(uuid.uuid4()))
	workflow = addTask(task, links, workflow)

	# Set UID of workflow so it lives in the same space in memory
	workflow.setWorkflowID(workflowID)
	
	# Serialize the workflow into json file
	serialize(workflow)
	
	# Get output of workflow
	output = workflow().__str__()
	splitOutput = output.split(',')
	result = []
	for o in splitOutput:
		if(".nc" in o):
			keyVal = o.split(": ")
			val = keyVal[1]
			val = val[1:len(val)-1]
			result.append(val)
		else:
			result.append(re.findall("[-+]?\d*\.\d+|\d+", output)[0])
			
	# open mongodb client and database
	client = MongoClient()
	db = client.testdb
	collection = db.testcollection
	
	# either update the workflow or create it if it doesn't exist	
	collection.update_one({'_id': workflowID}, {'$set': {'repop': repop}, {'data': workflow__list()__}}, upsert = True, multi = False)

	# Return the result, list representation of the workflow, and UID of the added task
	return {"result":result, "list":workflow.__list__(), "taskID": task.uid}
