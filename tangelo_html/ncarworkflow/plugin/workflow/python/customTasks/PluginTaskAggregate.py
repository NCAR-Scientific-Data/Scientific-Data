import subprocess
import pyutilib.workflow
import os

#   Class: taskAggregate
#   A task class that aggregates data.
#
#   Attributes:
#   
#       filename - the name of the NetCDF file to aggregate.
#       variable - the variable to aggregate.
#       interval - the time interval to aggregate over.
#       method - the method of aggregation.
#       outtime - the outtime
#       cyclic - whatever that means
#       result - the resulting output.
class PluginTaskAggregate(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskAggregate")
    alias = "taskAggregate"
    #   Constructor: __init__
    #   Creates an Aggregation task.
    #
    #   Parameters:
    #
    #       self - a reference to the object.
    #       *args - a list of arguments
    #       **kwds - a list of keyword arguments.
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

        args = ['ncl', '-n', '-Q', wid, tid, sFilename, sVariable, sInterval, sMethod, sOuttime, sCyclic, 'ncl/aggregate.ncl']
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
        result = "/data/{0}/{1}_aggregate.nc".format(self.workflowID,self.uid)
        if not sysError or not nclError:
            if not os.path.isfile(result):
                error = "NCL Error: Please check input parameters."
                nclError = True
        if nclError or sysError:
                self.result = error
        else:
                self.result = result