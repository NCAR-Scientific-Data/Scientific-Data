import subprocess
import pyutilib.workflow
import os
import tangelo

#   Class: PluginTaskSubset
#   A template for implementing new tasks
#
#   Attributes:
#
#       url - the OPeNDAP url for the netCDF file to subset.
#       variable - the variable to subset.
#       swlat - the southwest latitude coordinate of the bounding box to subset.
#       swlon - the southwest longitude coordinate of the bounding box to subset.
#       nelat - the northeast latitude coordinate of the bounding box to subset.
#       nelon - the northeast longitude coordinate of the bounding box to subset.
#       startdate - the beginning date to subset data over.
#       enddate - the final date to subset data over.
#       result - the output subsetted NetCDF file.
class PluginTaskTemplate(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskTemplate")
    alias = "taskTemplate"
    #   Constructor: __init__
    #   Creates a Template Task
    #
    #   Parameters:
    #
    #       self - a reference to the object.
    #       *args - a list of arguments
    #       **kwds - a list of keyword arguments.
    def __init__(self,*args,**kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('input1')
        self.inputs.declare('input2')
        self.inputs.declare('input3')
        self.outputs.declare('output1')

    #   Function: execute
    #   Calls an outside language to process data
    #
    #   Parameters:
    #
    #       self - a reference to the object.
    #
    #    Returns:
    #
    #       The path of the resulting subsetted NetCDF file
    def execute(self):
        swLat = "swLat={0}".format(str(self.swlat))
        swLon = "swLon={0}".format(str(self.swlon))
        neLat = "neLat={0}".format(str(self.nelat))
        neLon = "neLon={0}".format(str(self.nelon))
        filename = "filename=\"{0}\"".format(str(self.url))
        
        # List of args to pass to subprocess
        args = ['ncl', '-n', '-Q', filename, swLat, swLon, neLat, neLon '../plugin/workflow/python/customTasks/ncl/subset_time_latlon.ncl']

        # NCL
        # Open a subprocess to call arguments
        try:
            status = subprocess.call(args)
        # Catch errors
        except:
            sysError = True
            error = "System Error: Please contact the site administrator"
        if not sysError:
            # Common NCL errors
            if status:
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
                else:
                    error = "NCL Error - Error with NCL script"
                nclError = True

        # Save the resulting NetCDF
        result = "data/{0}/{1}_subset.nc".format(self.workflowID, self.uid)
        if not sysError or not nclError:
            if not os.path.isfile(result):
                error = "NCL Error - Error with NCL script"
                nclError = True
        if nclError or sysError:
            self.subset = error
        else:
            self.subset = result