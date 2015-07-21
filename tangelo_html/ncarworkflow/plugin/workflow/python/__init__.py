# Title: Workflow Library

import tangelo
import pyutilib.workflow
import json
import unicodedata
import ast
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
def addTask(task, links, output, workflow):
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

    for i in task.outputs:
        if output[i] != 'None':
            task.outputs[i] = output[i]
            task.set_ready()
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

            taskList.append((t, task["Inputs"], task["Outputs"]))
    
    for task in taskList:
        addTask(task[0], task[1], task[2], q)

    return q

#   Function: deserializeChangeTaskLinks
#   A function that builds a workflow from its json representation and changes
#   the inputs of a specified task to newly provided inputs.
#
#   Parameters:
#   
#       workflowString - The json dictionary representation of a workflow to be built
#       taskUID - the UID of the task to be modified
#       links - the new inputs for the specified task.
#
#   Returns:
#
#       q - A new instance of the workflow built from its representation
def deserializeChangeTaskLinks(workflowString, taskUID, links): 
    data = json.loads(workflowString)

    links = ast.literal_eval(links)
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
        if(task[0].UID() in [taskUID]):
            addTask(task[0], links, q)
        else:
            addTask(task[0], task[1], q)

    return q


#   Function: serialize
#   Takes a workflow object and builds it into a JSON string.
#
#   Parameters:
#   
#       workflow - the pyutilib workflow object to be serialized
#
#   Returns:
#
#       The workflow as a json-formatted dictionary via dumps()
def serialize(workflow):
    #with open('/data/'+ str(workflow.workflowID) +'.json', 'w') as outfile:
    return json.dumps(workflow.__dict__())

#   Function: getInstance
#   A wrapper function for the pyutilib.workflow.TaskFactory. Builds tasks based
#   on task types.
#
#   Parameters:
#   
#		taskType - a task type to be created by TaskFactory

#   Returns:
#
#       The new task as a pyutilib Task
def getInstance(taskType):
    return pyutilib.workflow.TaskFactory(taskType)

#   Function: createWorkflow
#   Creates a new pyutilib workflow object for populating with tasks
#
#   Parameters:
#   
#       None
#
#   Returns:
#
#       The new workflow object
def createWorkflow():
    return pyutilib.workflow.Workflow()

#   Function: loadWorkflow
#   A function that loads a mongo client instance, opens database 'database',
#	collection 'workflows', finds the workflow by searching for the workflowID,
#	and returns the repopulation data and json-formatted workflow data
#
#   Parameters:
#   
#       workflowID - the unique ID given to any new workflow
#
#   Returns:
#
#       (document['repop'], document['data']) - a tuple consisting of the repopulation 
#       data from the 'document' dictionary and the json formatted workflow data, 
#       respectively.
def loadWorkflow(workflowID):
	# open mongodb client and database
	client = MongoClient()
	db = client.database
	collection = db.workflows
	
	# find the workflow
	document = collection.find_one({"_id": workflowID})
	return (document['repop'], document['data'])

#   Function: saveWorkflow
#   A function that takes in the unique workflow ID, the json-formatted workflow data,
#	the repopulation data, and inserts the the workflow as a new document in MongoDB
#	if no existing document is found.
#
#   Parameters:
#   
#       workflowID - the unique ID given to any new workflow
#		data - the json-formatted workflow data
#		repop - the repopulation data for visualization
#
#   Returns:
#
#       function 'update_one' - will search for a workflow in the collection with
#		the workflowID, and either update the found workflow or insert a new document
#		with the parameters inputted.
def saveWorkflow(workflowID, data, repop):
	# open mongodb client and database
	client = MongoClient()
	db = client.database
	collection = db.workflows
	
	# save the workflow (upsert = True ensures an insert if no update possible)
	return collection.update_one({"_id": workflowID}, {'$set': {'data': data, 'repop': repop}}, upsert = True)

#   Function: addTaskNewLinks
#   A function that adds a task and sets the inputs of a task if and only if the
#   inputs are not the deleted task.
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

#   Function: buildUpdated
#   A function that rebuilds a workflow, only adding a task if and only if it
#   is not the deleted task.
#
#   Parameters:
#   
#       taskUID - The UID of the task to be deleted
#       worfklowString - The ID of the workflow to delete the task from
#
#   Returns:
#
#       q - An instance of a workflow built from its representation
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

#   Function: deleteTask
#   A function that deletes a task from a workflow.
#
#   Parameters:
#   
#       taskUID - UID of task to be deleted
#       workflowID - ID of the workflow for the task to be deleted from
#       workflowString - ID of the workflow for the task to be deleted from
#
#   Returns:
#
#       workflow - An instance of a workflow built from its representation
def deleteTask(taskUID, workflowID, workflowString):
    workflow = buildUpdatedWorkflow(taskUID, workflowID, workflowString)
    workflow.setWorkflowID(workflowID)
    return workflow
