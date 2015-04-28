import uuid
import json
import ast
import tangelo

#   Function: createWorkflow
#   A function that creates a new empty workflow
#
#   Returns:
#
#       (w, uid) - A tuple with an empty instance of a workflow and its UID
def createWorkflow():
    uid = uuid.uuid4()
    w = tangelo.plugin.workflow.createWorkflow()
    w.setWorkflowID(uid)
    return (w, uid)


# Call this function to add a new task to a workflow
#   Function: addTask
#   A function that adds a task of type taskType with inputs in 
#   links to a workflow instance "workflow" with the id = workflowID
#
#   Parameters:
#   
#       taskType - Type of task to be added
#       links - Dictionary of links and inputs for the new task
#       workflow - Instance of the workflow to add task to
#       workflowID - ID of the workflow to be built upon
#
#   Returns:
#
#       (workflow, task.uid) - A tuple with an instance of a workflow built from its representation and the new tasks UID
def addTask(taskType, links, workflow, workflowID):
    # Build workflow with filename workflowID.json
    #workflow = tangelo.plugin.workflow.deserialize(tangelo.store()[workflowID])
    # Add task to the workflow
    
    links = ast.literal_eval(links)

    # MAKE the task input be a type and call a factory to get instance of task
    task = tangelo.plugin.workflow.getInstance(taskType)
    task.setUID(str(uuid.uuid4()))
    task.setWorkflowID(workflowID)
    workflow = tangelo.plugin.workflow.addTask(task, links, workflow)

    # Set UID of workflow so it lives in the same space in memory
    workflow.setWorkflowID(workflowID)
    # Serialize the workflow into json file
    #tangelo.store()[workflowID] = tangelo.plugin.workflow.serialize(workflow)
    
    

    # Return the result, list representation of the workflow, and UID of the added task
    return (workflow, task.uid)

#   Function: deleteTask
#   A function that helps with rebuilding a workflow when deleting a task.
#   Call this function to delete a task
#
#   Parameters:
#   
#       taskUID - UID of task to be deleted
#       workflowID - ID of the workflow for the task to be deleted from
#
#   Returns:
#
#       workflow - An instance of a workflow built from its representation
def deleteTask(taskUID, workflowID):
    # Build workflow with filename workflowUID.json
    # Don't add task with UID = taskUID
    w = tangelo.plugin.workflow.deleteTask(taskUID, workflowID)
    return w

def getOutput(workflow):
    # Get output of workflow
    output = workflow().__str__()
    output = output.replace(" ", "")
    output = output.replace("'", "")

    resultList = [tuple(u.split(':')) for u in output.split("\n")]

    result = resultList[0][1] if len(resultList[0]) > 1 else resultList
    return result

def run(function, workflowID, args):
    w = None
    args = ast.literal_eval(args)
    if function == "createWorkflow":
        (w, uid) = createWorkflow()
        tangelo.store()[str(uid)] = tangelo.plugin.workflow.serialize(w)
        return {"uid": str(uid)}
    elif workflowID in tangelo.store():

        w = tangelo.plugin.workflow.deserialize(tangelo.store()[workflowID])
        
        if function == "addTask":
            (w, tid) = addTask(args[0], args[1], w, workflowID)
            tangelo.store()[workflowID] = tangelo.plugin.workflow.serialize(w)
            result = getOutput(w)
            return {"result":result, "workflow":w.__list__(), "taskID": tid}

        if function == "deleteTask":
            (w) = tangelo.plugin.workflow.deleteTask(args[0], workflowID, tangelo.store()[workflowID])
            tangelo.store()[workflowID] = tangelo.plugin.workflow.serialize(w)
            result = getOutput(w)
            return {"result":result, "workflow":w.__list__()}
    else:
        return {"Error": "Error - Could Not Update Workflow"}


w = pyutilib.workflow.Workflow()
