import uuid
import json
import ast
#import tangelo
import pyutilib.workflow

class TaskA(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('a')
        self.inputs.declare('b')
        self.outputs.declare('c')
    def execute(self):
        """Compute the sum of the inputs."""
        self.c = "test.nc"

class TaskB(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('d')
        self.outputs.declare('e')
    def execute(self):
        """Compute the sum of the inputs."""
        self.e = self.d*3

class TaskC(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('e')
        self.inputs.declare('c')
        self.outputs.declare('f')
    def execute(self):
        """Compute the sum of the inputs."""
        self.f = self.e*self.c

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

def updateTask(workflow, workflowID, taskUID, links):
    w = deserialize(workflowID)
    workflow = w.__dict__()
    for task in workflow:
        for key in task:
            if key in ['UID'] and task[key] in [taskUID]:
                task['Inputs'] = links 
    return workflow


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
w.setWorkflowID(str(uuid.uuid4()))

A = TaskA()
A.setUID(str(uuid.uuid4()))
A.setWorkflowID(w.workflowID)
B = TaskB()
B.setUID(str(uuid.uuid4()))
B.setWorkflowID(w.workflowID)
C = TaskC()
C.setUID(str(uuid.uuid4()))
C.setWorkflowID(w.workflowID)

A.inputs.a = 1
A.inputs.b = 2
B.inputs.d = A.outputs.c
C.inputs.e = B.outputs.e
C.inputs.c = 3

w.add(A)
w.add(B)
w.add(C)
updateTask(w.__dict__(), B.uid, {"d": [50]})