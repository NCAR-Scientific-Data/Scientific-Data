import test
import pyutilib.workflow
import uuid
import json
import re
import subprocess
#import pyutilib.workflow
import os
import rpy2.robjects as ro
import ast

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
            task.inputs[i] = links[i][0]

    # Add updated task to workflow and return new workflow
    workflow.add(task)
    return workflow

# Build a workflow from json file with id workflowID
def deserialize(workflowID):
    with open('data/'+workflowID+'.json') as data_file:    
        data = json.load(data_file)

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
            addTask(t, task['Inputs'], q)
    return q

# Serialize workflow into json file with UID as filename
def serialize(workflow):
    with open('data/'+workflow.workflowID+'.json', 'w') as outfile:
        json.dump(workflow.__dict__(), outfile)

# Call this function to add a new task to a workflow
def run(taskType, links, workflowID):
    # Build workflow with filename workflowID.json
    workflow = deserialize(workflowID)
    # Add task to the workflow
    
    links = ast.literal_eval(links)

    # MAKE the task input be a type and call a factory to get instance of task
    task = getInstance(taskType)
    task.setUID(str(uuid.uuid4()))
    task.setWorkflowID(workflowID)
    workflow = addTask(task, links, workflow)

    # Set UID of workflow so it lives in the same space in memory
    workflow.setWorkflowID(workflowID)
    # Serialize the workflow into json file
    serialize(workflow)
    
    # Get output of workflow
    output = workflow().__str__()
    splitOutput = output.split(',')
    result = []
    for o in splitOutput:
        if(".nc" in o):
            keyVal = o.split(": ")
            val = keyVal[1]
            val = val[1:len(val)-1]
            result.append(val)
        else:
            result.append(re.findall("[-+]?\d*\.\d+|\d+", output)[0])

    # Return the result, list representation of the workflow, and UID of the added task
    return {"result":result, "list":workflow.__list__(), "taskID": task.uid}

class taskSubset(pyutilib.workflow.Task):
    def __init__(self,*args,**kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('url')
        self.inputs.declare('variable')
        self.inputs.declare('swlat')
        self.inputs.declare('swlon')
        self.inputs.declare('nelat')
        self.inputs.declare('nelon')
        self.inputs.declare('startdate')
        self.inputs.declare('enddate')
        self.outputs.declare('subset')

    def execute(self):
        swLat = "swLat={0}".format(self.swlat)
        swLon = "swLon={0}".format(self.swlon)
        neLat = "neLat={0}".format(self.nelat)
        neLon = "neLon={0}".format(self.nelon)
        startDate = "startDate=\"{0}\"".format(self.startdate)
        endDate = "endDate=\"{0}\"".format(self.enddate)
        filename = "filename=\"{0}\"".format(self.url)
        v = "variable=\"{0}\"".format(self.variable)
        wid = "wid=\"{0}\"".format(self.workflowID)
        tid = "tid=\"{0}\"".format(self.id)
        
        args = ['ncl', '-n', '-Q', filename, v, swLat, swLon, neLat, neLon, startDate, endDate, wid, tid, '../ncl/subset_time_latlon.ncl']
        args = filter(None,args)
        sysError = False
        nclError = False

        try:
            status = subprocess.call(args)
        except:
            sysError = True
            error = "System Error: Please contact the site administrator"
        if not sysError:
            if status:
                if status == 2:
                    error = "NCL Error: Missing input parameter"
                elif status == 3:
                    error = "NCL Error: Lat/Lon values out of range"
                elif status == 4:
                    error = "NCL Error: Date value out of range"
                elif status == 5:
                    error = "NCL Error: Invalid parameter value"
                elif status == 6:
                    error = "NCL Error: Conversion error"
                else:
                    error = "NCL Error: Error with NCL script"
                nclError = True
        result = "data/{0}/{1}_subset.nc".format(self.workflowID, self.id)
        if not sysError or not nclError:
            if not os.path.isfile(result):
                error = "NCL Error: Error with NCL script"
                nclError = True
        if nclError or sysError:
            self.subset = error
        else:
            self.subset = result

#   Class: taskAggregate
#   A task class that aggregates data.
#
#   Attributes:
#   
#       filename - the name of the netCDF file to aggregate.
#       variable - the variable to aggregate.
#       interval - the time interval to aggregate over.
#       method - the method of aggregation.
#       outtime - the outtime
#       cyclic - whatever that means
#       result - the resulting output.
class taskAggregate(pyutilib.workflow.Task):

    #   Constructor: __init__
    #   Creates an Aggregation task.
    #
    #   Parameters:
    #
    #       self - a reference to the object.
    #       *args - a list of arguments
    #       **kwds - the number of arguments?
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('variable')
        self.inputs.declare('interval')
        self.inputs.declare('method')
        self.inputs.declare('outtime')
        self.inputs.declare('cyclic')
        self.outputs.declare('result')

    #   Function: execute
    #   Calls the NCL script to aggregate the data.
    #
    #   Parameters:
    #
    #       self - a reference to the object.
    #
    #    Returns:
    #
    #       The result.
    def execute(self):
        sFilename = "filename=\"{0}\"".format(self.filename)
        sInterval = "interval=\"{0}\"".format(self.interval)
        if not self.method:
                sMethod = ""
        else:
                sMethod = "method=\"{0}\"".format(self.method)
        if not self.outtime:
                sOuttime = ""
        else:
                sOuttime = "outtime=\"{0}\"".format(self.outtime)
        sCyclic = "cyclic={0}".format(self.cyclic)
        sVariable = "variable=\"{0}\"".format(self.variable)
        wid = "wid=\"{0}\"".format(self.workflowID)
        tid = "tid=\"{0}\"".format(self.uid)

        args = ['ncl', '-n', '-Q', wid, tid, sFilename, sVariable, sInterval, sMethod, sOuttime, sCyclic, '../ncl/aggregate.ncl']
        args = filter(None,args)
        sysError = False
        nclError = False

        try:
                status = subprocess.call(args)
        except:
                sysError = True
                error = "System Error: Please contact site administrator."
        if not sysError:
            if status:
                if status == 2:
                    error = "NCL Error: Missing input parameter"
                elif status == 3:
                    error = "NCL Error: Lat/Lon values out of range"
                elif status == 4:
                    error = "NCL Error: Date value out of range"
                elif status == 5:
                    error = "NCL Error: Invalid parameter value"
                elif status == 6:
                    error = "NCL Error: Conversion error"
                else:
                    error = "NCL Error: Error with NCL script"
                nclError = True
        result = "data/{0}/{1}_aggregate.nc".format(self.workflowID,self.uid)
        if not sysError or not nclError:
            if not os.path.isfile(result):
                error = "NCL Error: Please check input parameters."
                nclError = True
        if nclError or sysError:
                self.result = error
        else:
                self.result = result

class taskUnitConversion(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('variable')
        self.inputs.declare('outunit')
        self.outputs.declare('result')

    def execute(self):
            sFilename = "filename=\"{0}\"".format(self.filename)
            sVariable = "variable=\"{0}\"".format(self.variable)
            sOutunit = "outunit=\"{0}\"".format(self.outunit)
            wid = "wid=\"{0}\"".format(self.workflowID)
            tid = "tid=\"{0}\"".format(self.uid)
            
            args = ['ncl', '-n', '-Q', wid, tid, sFilename, sVariable, sOutunit, '../ncl/unit_conversion.ncl']
            args = filter(None,args)
            sysError = False
            nclError = False

            try:
                    status = subprocess.call(args)
            except:
                    sysError = True
                    error = "System Error: Please contact site administrator."
            if not sysError:
                if status:
                    if status == 2:
                        error = "NCL Error: Missing input parameter"
                    elif status == 3:
                        error = "NCL Error: Lat/Lon values out of range"
                    elif status == 4:
                        error = "NCL Error: Date value out of range"
                    elif status == 5:
                        error = "NCL Error: Invalid parameter value"
                    elif status == 6:
                        error = "NCL Error: Conversion error"
                    else:
                        error = "NCL Error: Error with NCL script"
                    nclError = True
            result = "data/{0}/{1}_unitconv.nc".format(self.workflowID,self.uid)
            if not sysError or not nclError:
                if not os.path.isfile(result):
                    error = "NCL Error: Please check input parameters."
                    nclError = True
            if nclError or sysError:
                    self.result = error 
            else:
                    self.result = result

class taskThreshold(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('field')
        self.inputs.declare('lower')
        self.inputs.declare('upper')

    def execute(self):
        # Check if user entered lowerlimit and upperlimit, if not
        #   Set lower to min or upper to max
        lowerlimit = str(self.lower) if self.lower else "min"
        upperlimit = str(self.upper) if self.upper else "max"

        # Import the R script so we can use its function
        scriptname = "tangelo_html/demo/r/calculate_threshold.R"
        ro.r['source'](scriptname)

        # Call the function that does the calculation
        value = ro.r['rfunc'](self.filename, self.field, lowerlimit, upperlimit)

#   Class: taskPlot
#   A task that plots.
class taskPlot(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('filename')
        self.inputs.declare('timeindex')
        self.inputs.declare('native')
        self.outputs.declare('result')
        
    def execute(self):
        sFilename = "filename=\"{0}\"".format(self.filename)
        if not self.timeindex:
                sTimeindex = "timeindex=0"
        else:
                sTimeindex = "timeindex={0}".format(self.timeindex)
        if self.native:
                plotScript = '../ncl/plot_native.ncl'
        else:
                plotScript = '../ncl/plot.ncl'
        wid = "wid=\"{0}\"".format(self.workflowID)
        tid = "tid=\"{0}\"".format(self.id)

        args = ['ncl', '-n','-Q', wid, tid, sFilename, sTimeindex, plotScript]
        args = filter(None,args)
        sysError = False
        nclError = False

        try:
                status = subprocess.call(args)
        except:
                sysError = True
                error = "System error, please contact site administrator."
        if self.native:
                result = "data/{0}/{1}_nativeplot.png".format(wid,tid)
        else:
                result = "data/{0}/{1}_plot.png".format(self.workflowID,self.id)
        if not sysError:
            if status:
                if status == 2:
                    error = "NCL Error: Missing input parameter"
                elif status == 3:
                    error = "NCL Error: Lat/Lon values out of range"
                elif status == 4:
                    error = "NCL Error: Date value out of range"
                elif status == 5:
                    error = "NCL Error: Invalid parameter value"
                elif status == 6:
                    error = "NCL Error: Conversion error"
                else:
                    error = "NCL Error: Error with NCL script"
                nclError = True
        if not sysError or not nclError:
            if not os.path.isfile(result):
                error = "NCL Error: Please check input parameters."
                nclError = True
        if nclError or sysError:
                self.result = error
        else:
                self.result = result

def getInstance(taskType):
    if taskType == "taskSubset":
        return taskSubset()
    elif taskType == "taskAggregate":
        return taskAggregate()
    elif taskType == "taskUnitConversion":
        return taskUnitConversion()
    elif taskType == "taskThreshold":
        return taskThreshold()
    else:
        return None

