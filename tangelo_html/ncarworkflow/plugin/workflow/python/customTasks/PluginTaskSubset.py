import subprocess
import pyutilib.workflow
import os
import tangelo

#   Class: PluginTaskSubset
#   A task class that subsets NetCDF data.
#
#   Attributes:
#
#       url - The OPeNDAP url for the netCDF file to subset.
#       variable - The variable to subset.
#       swlat - The southwest latitude coordinate of the bounding box to subset.
#       swlon - The southwest longitude coordinate of the bounding box to subset.
#       nelat - The northeast latitude coordinate of the bounding box to subset.
#       nelon - The northeast longitude coordinate of the bounding box to subset.
#       startdate - The beginning date to subset data over.
#       enddate - The final date to subset data over.
#       result - The output subsetted NetCDF file.
class PluginTaskSubset(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskSubset")
    alias = "taskSubset"
    #   Constructor: __init__
    #   Creates a Subset task
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #       *args - A list of arguments.
    #       **kwds - A list of keyword arguments.
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

    #   Function: execute
    #   Calls the NCL script to subset the NetCDF file.
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #
    #    Returns:
    #
    #       The path of the resulting subsetted NetCDF file.
    def execute(self):
        swLat = "swLat={0}".format(str(self.swlat))
        swLon = "swLon={0}".format(str(self.swlon))
        neLat = "neLat={0}".format(str(self.nelat))
        neLon = "neLon={0}".format(str(self.nelon))
        startDate = "startDate=\"{0}\"".format(str(self.startdate))
        endDate = "endDate=\"{0}\"".format(str(self.enddate))
        filename = "filename=\"{0}\"".format(str(self.url))
        v = "variable=\"{0}\"".format(str(self.variable))
        wid = "wid=\"{0}\"".format(self.workflowID)
        tid = "tid=\"{0}\"".format(self.uid)
        
        args = ['ncl', '-Q', filename, v, swLat, swLon, neLat, neLon, startDate, endDate, wid, tid, '../plugin/workflow/python/customTasks/ncl/subset_time_latlon.ncl']
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
        result = "data/{0}/{1}_subset.nc".format(self.workflowID, self.uid)
        if not sysError or not nclError:
            if not os.path.isfile(result):
                error = "NCL Error - Error with NCL script "
                nclError = True
        if nclError or sysError:
            self.subset = error
        else:
            self.subset = result