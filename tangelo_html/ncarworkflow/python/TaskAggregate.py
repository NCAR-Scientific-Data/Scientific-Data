#    File: TaskAggregate.py
#    This script Aggregates data in from a given NetCDF file via a NCL script. The NCL script
#    takes in an input file, output file, the variable on which to aggregate, the method to use (mean, min, max),
#    the interval on which to aggregate (day, month, season, or year), and the outtime to set (the date/time of interval
#    to set the aggregate result). The output file is then a NetCDF with the aggregate data

import subprocess
import sys
import re
import pyutilib.workflow
import os



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
        wid = "wid={0}".format(self.workflowID)
        tid = "tid={0}".format(self.id)

        args = ['ncl', '-n', '-Q', wid, tid, sFilename, sVariable, sInterval, sMethod, sOuttime, sCyclic, 'ncl/aggregate.ncl']
        args = filter(None,args)
        sysError = False
        nclError = False
        try:
                status = subprocess.check_call(args)
        except:
                sysError = True
                error = "System Error: Please contact site administrator."

        result = "/data/{0}/{1}_aggregate.nc".format(self.workflowID,self.id)
        if not sysError:
            if not os.path.isfile(result):
                error = "NCL Error: Please check input parameters."
                nclError = True
        if nclError or sysError:
                self.result = error
        else:
                self.result = result