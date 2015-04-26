import tangelo
import pyutilib.workflow
import json
import unicodedata
from customTasks import  *

from pymongo import MongoClient

# Add task with linkks to workflow
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
            task.inputs[i] = links[i]

    # Add updated task to workflow and return new workflow
    workflow.add(task)
    return workflow

# Build a workflow from json file with id workflowID
def deserialize(workflowString): 
    data = json.loads(workflowString)

    taskList = []
    # Create temp workflow
    q = pyutilib.workflow.Workflow()
    for task in data:
        # Dont recreate empty tasks (done for you)
        if not task['Type'] in ['EmptyTask']:
            # Create instance of specified task
            # TODO:
            # Make this a factory and replace with actual tasks
            t = getInstance(task['Type'])
            # Set UID to its previous instance's
            # This is so the particular task in the workflow
            # will always be linked properly
            t.setUID(task['UID'])
            t.setWorkflowID(task['WorkflowID'])
            # Add task t to workflow q with proper inputs
            for key, value in task["Inputs"].iteritems():
                if value[0] != "Port":
                    task["Inputs"][key] = value[0].encode("ascii", "ignore")
                else:
                    task["Inputs"][key] = ["Port", value[1].encode("ascii", "ignore"), value[2].encode("ascii", "ignore")]

            taskList.append((t, task["Inputs"]))
    
    for task in taskList:
        addTask(task[0], task[1], q)

    return q

# Serialize workflow into json file with UID as filename
def serialize(workflow):
    #with open('/data/'+ str(workflow.workflowID) +'.json', 'w') as outfile:
    return json.dumps(workflow.__dict__())

def getInstance(taskType):
    return pyutilib.workflow.TaskFactory(taskType)

def createWorkflow():
    return pyutilib.workflow.Workflow()
    
def loadWorkflow(workflowID):
	# open mongodb client and database
	client = MongoClient()
	db = client.database
	collection = db.workflows
	
	document = collection.find_one({"_id": workflowID}).strip("u")
	return {"repop": document['repop'], "data": document['data']}
	
def saveWorkflow(workflowID, data, repop):
	# open mongodb client and database
	client = MongoClient()
	db = client.database
	collection = db.workflows
	
	return collection.update_one({"_id": workflowID}, {'$set': {'data': data, 'repop': repop}}, upsert = True)
