#  _________________________________________________________________________
#
#  PyUtilib: A Python utility library.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  _________________________________________________________________________

"""Definitions for workflow task objects."""

__all__ = ['Task', 'EmptyTask', 'Component']

import argparse
import pprint
import re
import uuid
from pyutilib.workflow import globals
from pyutilib.misc import Options
from pyutilib.workflow import port 


class Task(object):
    """
    A Task object represents a single action in a workflow.
    """

    def __init__(self, id=None, name=None, parser=None):
        """Constructor."""
        if not id is None:
            self.id = id
        else:
            self.id = globals.unique_id()
        if name is None:
            self.name = "Task"+str(self.id)
        else:
            self.name = name
        self.inputs = port.InputPorts(self)
        self.inputs.set_name(self.name+"-inputs")
        self.outputs = port.OutputPorts(self)
        self.outputs.set_name(self.name+"-outputs")
        self._resources = {}
        self._predecessors = []
        self._create_parser(parser)
        self.input_controls = port.InputPorts(self)
        self.input_controls.set_name(self.name+'-input-controls')
        self.output_controls = port.OutputPorts(self)
        self.output_controls.set_name(self.name+'-output-controls')
        self.debug = False
        # Robert Crimi
        self.workflowID = None
        self.uid = str(uuid.uuid4())

    def add_resource(self, resource):
        """Add a resource that is required for this task to execute."""
        self._resources[resource.name] = resource

    def resource(self, name):
        """Return the specified resource object."""
        return self._resources[name]

    def next_tasks(self):
        """Return the set of tasks that succeed this task in the workflow."""
        return set([t.to_port.task() for name in self.outputs for t in self.outputs[name].output_connections]) | set([t.to_port.task() for name in self.output_controls for t in self.output_controls[name].output_connections])
            
    def prev_tasks(self):
        """Return the set of tasks that precede this task in the workflow."""
        return set([task for name in self.inputs for task in self.inputs[name].from_tasks() if task.id != NoTask.id]) | set(task for task in self._predecessors) | set([task for name in self.input_controls for task in self.input_controls[name].from_tasks() if task.id != NoTask.id])
           
    def next_task_ids(self):
        """Return the set of ids for tasks that succeed this task in the workflow."""
        return set(task.id for task in self.next_tasks())

    # Robert Crimi
    def next_task_indices(self):
        return set((task.id-1) for task in self.next_tasks())

    # Robert Crimi
    def next_task_names(self):
        return set((task.alias + str(task.id)) if hasattr(task, "alias") else task.name for task in self.next_tasks())

    def prev_task_ids(self):
        """Return the set of ids for tasks that precede this task in the workflow."""
        return set(task.id for task in self.prev_tasks())

    # Robert Crimi
    def prev_task_names(self):
        return set((task.alias + str(task.id)) if hasattr(task, "alias") else task.name for task in self.prev_tasks())

    # Robert Crimi
    def setWorkflowID(self, workflow):
        self.workflowID = workflow

    # Robert Crimi
    def setUID(self, uid):
        self.uid = uid

    # Hannah T
    def getUID(self):
        return self.uid
           
    def execute(self, debug=False):
        """Execute this task."""
        raise ValueError("There is no default execution for an abstract Task object! Task=%s" % str(self))  #pragma:nocover

    def busy_resources(self):
        """Return the list of resources that this task is waiting for."""
        return [name for name in self._resources if not self._resources[name].available()]

    def ready(self):
        if self.busy():
            return False
        for name in self.inputs:
            #print "XYZ",self.name, name, self.inputs[name].ready(),self.inputs[name]._ready
            #for connection in self.inputs[name].input_connections:
                #print "XYZ",self.name, name,connection.from_port._ready, connection.ready(), len(connection.from_port.input_connections), connection.from_port.task.name
            if not self.inputs[name].ready():
                #print "FALSE - input", name
                #print self.inputs[name]
                return False
        for name in self.input_controls:
            if not self.input_controls[name].ready():
                #print "FALSE - control", name
                return False
        return True

    def busy(self):
        """Return the list of resources that this task is waiting for."""
        return len(self.busy_resources())

    def __call__(self, *options, **kwds):
        """Setup inputs and output parameters and execute this task.

        Copy the inputs into this Task's dictionary, then execute the task, then copy 
        the outputs out of the dictionary.
        """
        self._call_init(*options, **kwds)
        self.execute()
        return self._call_fini(*options, **kwds)

    def _call_init(self, *options, **kwds):
        self._call_start()
        busy = self.busy_resources()
        if len(busy) > 0:
            raise IOError("Cannot execute task %s.  Busy resources: %s" % (self.name, str(busy)))
        # Set inputs
        for opt in options:
            self._set_inputs(opt)
        self._set_inputs(kwds)
        #
        for name, res in self._resources.items():
            res.lock()
        for i in self.outputs:
            #print "z",i,getattr(self.outputs,i).get_value()
            setattr(self, i, None)
        for i in self.inputs:
            #print "OIUOX",i,self.inputs[i].get_value(),str(self.inputs[i])
            # TODO: validate that non-optional inputs have a value other than None
            self.inputs[i].compute_value()
            setattr(self, i, self.inputs[i].get_value())

    def _call_fini(self, *options, **kwds):
        for i in self.outputs:
            #print "Z",i,getattr(self.outputs,i).get_value()
            # TODO: validate that non-optional outputs have a value other than None
            self.outputs[i].set_value( getattr(self, i) )

        for name, res in self._resources.items():
            res.unlock()
        self._call_finish()
        self.set_ready( )
        #
        opt = Options()
        for i in self.outputs:
            setattr(opt, i, getattr(self.outputs,i).get_value())
        return opt

    def set_options(self, args):
        """Use a list of command-line options to initialize this task."""
        [self.options, args] = self._parser.parse_known_args(args)
        tmp = {}
        for action in self._parser._actions:
            try:
                val = getattr(self.options, action.dest)
                tmp[action.dest] = val
            except:
                pass
        self._set_inputs(tmp)

    def _call_start(self):
        """This method is executed when the task is started."""
        pass

    def _call_finish(self):
        """This method is executed when the task is finished."""
        pass

    def _set_inputs(self, options):
        """Set the inputs from a dictionary."""
        for key in options:
            self.inputs[key].set_value(options[key])

    def set_arguments(self, parser=None):
        if parser is None:
            return
        for arg in self._parser_arg:
            args = arg[0]
            kwargs = arg[1]
            self._parser.add_argument(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        self._parser_arg.append([args,kwargs])
        self._parser.add_argument(*args, **kwargs)

    def _create_parser(self, parser=None):
        """Create the OptionParser object and populated it with option groups."""
        if parser is None:
            self._parser = argparse.ArgumentParser()
        else:
            self._parser = parser
        self._parser_arg = []
        self._parser_group = {}
        self._create_parser_groups()
        for key in self._parser_group:
            self._parser.add_argument_group(self._parser_group[key])

    def _create_parser_groups(self):
        """This method is called by the _create_parser method to setup the
        parser groups that are registered for this task."""

    def _repn_(self):
        tmp = {}
        tmp['A_TYPE'] = 'Task'
        tmp['Name'] = self.name
        tmp['Id'] = self.id
        tmp['Inputs'] = self.inputs._repn_()
        tmp['Outputs'] = self.outputs._repn_()
        tmp['InputControls'] = self.input_controls._repn_()
        tmp['OutputControls'] = self.output_controls._repn_()
        return tmp 

    # Robert Crimi
    # Return dictionary for serialization of workflows
    def _dict_(self, workflow):
        tmp               = {}
        tmp['Type']       = self.alias if hasattr(self, "alias") else self.__class__.__name__
        tmp['Inputs']     = {}
        tmp['Outputs']    = {}
        tmp['WorkflowID'] = self.workflowID
        outputDictionary  = self.outputs._repn_()

        for key in outputDictionary:
            if key not in ['A_TYPE', 'Name', 'Mode', 'Owner']:
                val = outputDictionary[key]
                tmp['Outputs'][key] = val['Value']


        # Create dictionary of instances inputs
        dictionary = self.inputs._repn_()
        for key in dictionary:
            # Find the actual input values of the instance
            if not key in ['A_TYPE','Name','Mode','Owner']:
                val = dictionary[key]

                # Value is number
                # if re.match("^-?(\d*\.?\d+$)",val['Value']):
                #     val = [float(val['Value'])]
                # # TODO:
                # # handle files or other strings input into tasks
                # # Value is string
                # elif(".nc" in val['Value']):
                #     val = [val['Value']]

                # Value is port
                if val["Value"] == "None":
                    # Get the port connections
                    connection = dictionary[key]['Connections']['Inputs'][0]
                    link = re.findall("-?(\d*\.?\d+)", connection)
                    # Map strings to ints
                    link = list(map(int, link))

                    # Find UIDS of tasks with ids in link
                    
                    newLinks = workflow._dfs_([workflow._start_task.id], lambda t: t.getUIDWithID(link[0]))
                    # Set val to ['Port', UID, output]
                    val = ['Port', newLinks[0][0], newLinks[0][1][0]]
                else:
                    val = [val["Value"]]

                # Set inputs value to the link
                tmp['Inputs'][key] = val
        # If instance is not EmptyTask
        if not type(self) == EmptyTask:
            # Set unique identifier for this task
            tmp['UID'] = str(self.uid)
        return tmp

    # Robert Crimi
    def getTaskWithID(self, uid):
        if str(self.uid) == uid:
            return self

    # Robert Crimi
    def getUIDWithID(self, uid):
        if self.id == uid:
            # Get outputs
            os = []
            for key in self.outputs:
                if not key in ['A_TYPE','Name','Mode','Owner']:
                    os.append(key)
            # return [UID, outputs]
            return [self.uid, os]

    def __repr__(self):
        """Return a string representation for this task."""
        return pprint.pformat(self._repn_(), 2)

    def __str__(self):
        """Return a string representation for this task."""
        return "%s prev: %s next: %s resources: %s" % (str((self.alias + str(self.id)) if hasattr(self, "alias") else self.name),str(sorted(list(self.prev_task_names()))),str(sorted(list(self.next_task_names()))), str(sorted(self._resources.keys())))

    # Robert Crimi
    def __list__(self):
        return [self.alias if hasattr(self, "alias") else self.__class__.__name__, self.id-1, sorted(list(self.next_task_indices())), self.uid] 

    def reset(self):
        #print "RESETING "+self.name
        for i in self.outputs:
            self.outputs[i].reset()
        for i in self.output_controls:
            self.output_controls[i].reset()

    # Robert Crimi
    def reset_all(self):
        for i in self.outputs:
            self.outputs[i].reset_all()
            self.outputs[i].set_ready()
        for i in self.output_controls:
            self.output_controls[i].reset_all()
            self.output_controls[i].set_ready()
        for i in self.inputs:
            self.inputs[i].reset_all()
            self.inputs[i].set_ready()
        for i in self.input_controls:
            self.input_controls[i].reset_all()
            self.input_controls[i].set_ready()

    # Robert Crimi
    def reset_all_outputs(self):
        for i in self.outputs:
            self.outputs[i].reset_all()
            #self.outputs[i].set_ready()
        for i in self.output_controls:
            self.output_controls[i].reset_all()
            #self.output_controls[i].set_ready()                

    def set_ready(self):
        for i in self.outputs:
            self.outputs[i].set_ready()
        


class Component(Task):
    """
    Alias for the Task class.
    """

    def __init__(self, *args, **kwds):
        """Constructor."""
        Task.__init__(self, *args, **kwds)          #pragma:nocover


class EmptyTask(Task):

    def __init__(self, id=None, name=None):
        """Constructor."""
        Task.__init__(self, id=None, name=None)

    def __call__(self, *args, **kwds):
        """Empty task execution."""

# A task instance that represents no task.
NoTask = Task(id=0)

