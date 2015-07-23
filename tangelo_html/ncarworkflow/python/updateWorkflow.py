import uuid
import json
import ast
import tangelo
import pyutilib.workflow

#   Title: Update Workflow

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

#   Function: addTask
#   A function that creates a new task, declares the task's input values,
#   and adds the task to the workflow.
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
    # Add task to the workflow
    links = ast.literal_eval(links)

    task = tangelo.plugin.workflow.getInstance(taskType)
    task.setUID(str(uuid.uuid4()))
    task.setWorkflowID(workflowID)
    print "-"*100
    print task.workflowID
    workflow = tangelo.plugin.workflow.addTask(task, links, None, workflow)

    # Set UID of workflow so it lives in the same space in memory
    workflow.setWorkflowID(workflowID)

    # Return the workflow and the new task ID.
    return (workflow, task.uid)

#   Function: getOutput
#   Runs the workflow and parses the output of the workflow.
#
#   Parameters:
#   
#       workflow - The instance of the workflow to be run
#
#   Returns:
#
#       result - The output of the workflow
def getOutput(workflow):
    # Get output of workflow
    output = workflow().__str__()
    output = output.replace(" ", "")
    output = output.replace("'", "")

    resultList = [tuple(u.split(':')) for u in output.split("\n")]

    result = resultList[0][1] if len(resultList[0]) > 1 else resultList
    return result


#   Function: run
#   A function that delegates calls to the tangelo workflow plugin, saves temporary
#   workflows, and runs workflows.
#
#   Parameters:
#   
#       function - A string with the name of the function to be called. Possible Values: "createWorkflow," "saveWorkflow," "loadWorkflow," "addTask," "deleteTask," "updateTask"
#       workflowID - the Workflow ID.
#       args - The arguments to pass to the function call.
#
#   Returns:
#       
#       A Dictionary containing up to three values, depending on what function is
#       being performed.
#
#       createWorkflow - Returns the workflow unique ID.
#       saveWorkflow - Returns true or false depending on success.
#       loadWorkflow - Returns the result of the workflow, the workflow as a list, and the dictionary of repopulation values for tasks.
#       addTask - Returns the result of the workflow, the workflow as a list, and the task ID of the newly added task.
#       deleteTask - Returns the result of the workflow and the workflow as a list.
#       updateTask - Returns the result of the workflow and the workflow as a list.
#       
#       If there is an error, the dictionary returns an error message instead.
def run(function, workflowID, args):
    w = None
    args = ast.literal_eval(args)
    
    if function == "createWorkflow":

        (w, uid) = createWorkflow()
        tangelo.store()[str(uid)] = tangelo.plugin.workflow.serialize(w)
        return {"uid": str(uid)}

    elif function == "saveWorkflow":

        success = tangelo.plugin.workflow.saveWorkflow(workflowID, tangelo.store()[workflowID], args[0])
        if success:
            if tangelo.store().pop(workflowID, False) == False:
                return {"result" : "false"}
            return {"result": "true"}
        return {"result": "false"}

    elif function == "loadWorkflow":

        (repop, w) = tangelo.plugin.workflow.loadWorkflow(workflowID)
        tangelo.store()[workflowID] = w
        w = tangelo.plugin.workflow.deserialize(w)
        result = getOutput(w)

        return {"result": result, "workflow" : w.__list__(), "repop" : repop}

    elif workflowID in tangelo.store():

        w = tangelo.plugin.workflow.deserialize(tangelo.store()[workflowID])
        
        if function == "addTask":

            (w, tid) = addTask(args[0], args[1], w, workflowID)
            tangelo.store()[workflowID] = tangelo.plugin.workflow.serialize(w)
            result = getOutput(w)

            return {"result":result, "workflow":w.__list__(), "taskID": tid}
        elif function == "deleteTask":

            w = tangelo.plugin.workflow.deleteTask(args[0], workflowID, tangelo.store()[workflowID])
            tangelo.store()[workflowID] = tangelo.plugin.workflow.serialize(w)
            result = getOutput(w)

            return {"result":result, "workflow":w.__list__()}
        elif function == "updateTask":
            
            w = tangelo.plugin.workflow.deserializeChangeTaskLinks(tangelo.store()[workflowID], args[0], args[1])
            tangelo.store()[workflowID] = tangelo.plugin.workflow.serialize(w)
            result = getOutput(w)

            return {"result":result, "workflow":w.__list__()}
        else:
            return {"Error": "Error - Could Not Update Workflow"}

    else:
        return {"Error": "Error - Could Not Update Workflow"}


w = pyutilib.workflow.Workflow()
