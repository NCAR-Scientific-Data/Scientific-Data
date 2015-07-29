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
            
            args = ['/usr/local/ncl/bin/ncl', '-Q', wid, tid, sFilename, sUnit, '../plugin/workflow/python/customTasks/ncl/unit_conversion.ncl']
            args = filter(None,args)
            sysError = False
            nclError = False

            
            os.environ["NCARG_ROOT"] = '/usr/local/ncl'
            p  = subprocess.Popen(args, stdout=subprocess.PIPE)
            status, err = p.communicate()
            p.stdout.close()

            if err:
                error = "System Error: Please contact the site administrator"
            elif status:
                if status == 2:
                    error = "NCL Error - Missing input parameter"
                elif status == 3:
                    error = "NCL Error - Lat/Lon values out of range"
                elif status == 4:
                    error = "NCL Error - Date value out of range"
                elif status == 5:
                    error = "NCL Error - Invalid parameter value"
                elif status == 6:
                    error = "NCL Error - Conversion error"
                elif status == 7:
                    error = "NCL Error - Error Creating File"
                elif status == 8:
                    error = "NCL Error - Problem with OPeNDAP"
                else:
                    error = "NCL Error - Error with NCL script"
                nclError = True


            result = "data/{0}/{1}_unitconv.nc".format(self.workflowID,self.uid)
            if nclError or err:
                self.result = error
            else:
                self.result = result