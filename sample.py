import pyutilib.workflow
import json
import uuid
import pprint


class taskA(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskA")
    alias="taskA"

    def __init__(self,*args,**kwds):
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('a')
        self.inputs.declare('b')
        self.outputs.declare('c')


    def execute(self):
        self.c = self.a + self.b

class taskB(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskB")
    alias="taskB"

    def __init__(self,*args,**kwds):
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('d')
        self.inputs.declare('e')
        self.outputs.declare('f')


    def execute(self):
        self.f = float(self.d) * float(self.e)

class taskC(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskC")
    alias="taskC"

    def __init__(self,*args,**kwds):
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('g')
        self.outputs.declare('h')


    def execute(self):
        self.h = self.g*2

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
    return json.dumps(workflow.__dict__())

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
            t = pyutilib.workflow.TaskFactory(task['Type'])
            # Set UID to its previous instance's
            # This is so the particular task in the workflow will always be linked properly
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


w = pyutilib.workflow.Workflow()
uid = str(uuid.uuid4())
w.setWorkflowID(uid)
A = taskA()
A.setWorkflowID(w.workflowID)
A.setUID(str(uuid.uuid4()))
B = taskB()
B.setWorkflowID(w.workflowID)
B.setUID(str(uuid.uuid4()))

A.inputs.a = 2
A.inputs.b = 4
#B.inputs.d = A.outputs.c
#B.inputs.e = 2

w.add(A)
#w.add(B)

print "Original w"
print "-"*50
pprint.pprint(A.outputs.c._ready)
print w()
pprint.pprint(w.__dict__())

print "New w"
print "-"*50
serializedW = serialize(w)
deserializedW = deserialize(serializedW)
t = deserializedW._dfs_([deserializedW._start_task.id], lambda t: t.getTaskWithID(A.uid))
pprint.pprint(t[0].outputs.c._ready)
print deserializedW()
pprint.pprint(deserializedW.__dict__())


