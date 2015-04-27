import tangelo
import pyutilib.workflow
import json
import unicodedata
from customTasks import  *

from pymongo import MongoClient


#   Function: addTask
#   A function that adds a task with specified links to a workflow
#
#   Parameters:
#   
#       task - the instance of a task to add
#       links - the inputs to the specified task
#       workflow - the instance of the workflow to add the new task to
#
#   Returns:
#
#       workflow - An updated instance of the workflow with the new task added and linked
def addTask(task, links, workflow):
    for i in task.inputs:
        # Input is Port
        if(links[i][0] == 'Port'):
            # Find the task in the workflow with UID in link[i]
            t = workflow._dfs_([workflow._start_task.id], lambda t: t.getTaskWithID(links[i][1]))
            # Reset the tasks outputs
            #t[0].reset_all_outputs()
            # Set the input to the outputs of found task
            if len(t) > 0:
                task.inputs[i] = t[0].outputs[links[i][2]]
            else :
                task.inputs[i] = " "
                print "Couldn't find the task...you did something horribly wrong."
        # Input is number
        # TODO:
        # Better checking
        else:
            task.inputs[i] = links[i]

    # Add updated task to workflow and return new workflow
    workflow.add(task)
    return workflow


#   Function: deserialize
#   A function that builds a workflow from its json representation
#
#   Parameters:
#   
#       workflowString - The json dictionary representation of a workflow to be built
#
#   Returns:
#
#       q - An instance of a workflow built from its representation
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

#   Function: deserializeChangeTaskLinks
#   A function that builds a workflow from its json representation and sets inputs of
#   specified task to new links
#
#   Parameters:
#   
#       workflowString - The json dictionary representation of a workflow to be built
#       taskUID - the UID of the task to be modified
#       links - the new links for the specified task
#
#   Returns:
#
#       q - A new instance of the workflow built from its representation
def deserializeChangeTaskLinks(workflowString, taskUID, links): 
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
        if(task[0].UID in [taskUID]):
            addTask(task[0]), links, q)
        else:
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
	
	document = collection.find_one({"_id": workflowID})
	return (document['repop'], document['data'])
	
def saveWorkflow(workflowID, data, repop):
	# open mongodb client and database
	client = MongoClient()
	db = client.database
	collection = db.workflows
	
	return collection.update_one({"_id": workflowID}, {'$set': {'data': data, 'repop': repop}}, upsert = True)

#   Function: addTaskNewLinks
#   A function that helps with rebuilding a workflow when deleting a task.
#   Does not set links for task with link to a deleted task
#
#   Parameters:
#   
#       task - instance of task to be added
#       taskUID - UID of task to be checked for in links
#       links - inputs for the new task
#       workflow - instance of workflow for task to be added to
#
#   Returns:
#
#       workflow - An instance of a workflow built from its representation
def addTaskNewLinks(task, taskUID, links, workflow):
    for i in task.inputs:
        # Input is Port
        # links = ['Port', UID,] 
        if(links[i][0] == 'Port'):
            # Do not add link to deleted task with UID = taskUID
            if(not taskUID == links[i][1]):
                # Find the task in the workflow with UID in link[i]
                t = workflow._dfs_([workflow._start_task.id], lambda t: t.getTaskWithID(links[i][1]))[0]
                # Reset the tasks outputs
                #t.reset_all_outputs()
                # Set the input to the outputs of found task
                task.inputs[i] = t.outputs[links[i][2]]
            else:
                task.inputs[i] = " "

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
def buildUpdatedWorkflow(taskUID, workflowID, workflowString):
    data = json.loads(workflowString)
    # Create temp workflow
    q = pyutilib.workflow.Workflow()
    for task in data:
        # Dont recreate empty tasks (done for you)
        if (task['Type'] not in ['EmptyTask']) and (task['UID'] not in [taskUID]):
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
            addTaskNewLinks(t, taskUID, task['Inputs'], q)
    return q


def deleteTask(taskUID, workflowID, workflowString):
    workflow = buildUpdatedWorkflow(taskUID, workflowID, workflowString)
    workflow.setWorkflowID(workflowID)
    serialize(workflow)
    return workflow
