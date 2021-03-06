import subprocess
import pyutilib.workflow
import os

#   Class: PluginTaskUnitConversion
#   A task class that converts temperature units
#
#   Attributes:
#
#       filename - The name of the NetCDF file to convert.
#       outunit - The unit to convert the data to.
#       result - The resulting NetCDF file with new units.
class PluginTaskUnitConversion(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskUnitConversion")
    alias = "taskUnitConversion"
    #   Constructor: __init__
    #   Creates a UnitConversion task.
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #       *args - A list of arguments.
    #       **kwds - A list of keyword arguments.
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('unit')
        self.outputs.declare('result')

    #   Function: execute
    #   Calls the NCL script to convert the units of the data.
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #
    #   Returns:
    #
    #       The path of the resulting NetCDF file with converted units.
    def execute(self):
            sFilename = "filename=\"{0}\"".format(self.filename)
            sUnit = "unit=\"{0}\"".format(self.unit)
            wid = "wid=\"{0}\"".format(self.workflowID)
            tid = "tid=\"{0}\"".format(self.uid)
            
            args = ['ncl', '-Q', wid, tid, sFilename, sUnit, '../plugin/workflow/python/customTasks/ncl/unit_conversion.ncl']
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