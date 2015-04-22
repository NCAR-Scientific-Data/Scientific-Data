import uuid
import json
import ast
import tangelo

def createWorkflow():
    uid = uuid.uuid4()
    w = tangelo.plugin.workflow.createWorkflow()
    w.setWorkflowID(uid)
    return (w, uid)


# Call this function to add a new task to a workflow
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

def getOutput(workflow):
    # Get output of workflow
    output = workflow().__str__()
    output = output.replace(" ", "")
    output = output.replace("'", "")

    resultList = [tuple(u.split(':')) for u in output.split("\n")]

    result = resultList[0][1]
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
    else:
        return {"Error": "Error - Could Not Update Workflow"}
