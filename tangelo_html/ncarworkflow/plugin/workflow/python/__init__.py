import tangelo
import pyutilib.workflow
import json
import unicodedata
from customTasks import  *

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

# Add task with links to workflow
# Do not set link to deleted task
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
def buildUpdatedWorkflow(taskUID, workflowID, workflowString):
    data = json.parse(workflowString)
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
            addTaskNewLinks(t, taskUID, task['Inputs'], q)
    return q


def deleteTask(taskUID, workflowID, workflowString):
    workflow = buildUpdatedWorkflow(taskUID, workflowID, workflowString)
    workflow.setWorkflowID(workflowUID)
    serialize(workflow)
    return workflow


