import subprocess
import pyutilib.workflow
import os
import tangelo


def get_file_name_location(fileName):
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(scriptDir):
        if fileName in files:
            return os.path.join(root, fileName) + " "
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

        args = ['/usr/local/ncl-6.2.1/bin/ncl', '-Q', filename, v, swLat, swLon, neLat, neLon, startDate, endDate, wid, tid, get_file_name_location('subset_time_latlon.ncl')]
        args = filter(None,args)
        sysError = False
        nclError = False

        workflowDirName = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/python/data/" + self.workflowID + "/"
        if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)
        

        print "-"*100
        print args
        p  = subprocess.Popen(args, stdout=subprocess.PIPE)
        status, err = p.communicate()
        p.stdout.close()
        print "-"*100
        print status      
        if err:
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
                elif status == 7:
                    error = "NCL Error - Error Creating File"
                elif status == 8:
                    error = "NCL Error - Problem with OPeNDAP"
                else:
                    error = "NCL Error - Error with NCL script"
                nclError = True
        result = "data/{0}/{1}_subset.nc".format(self.workflowID, self.uid)

        if nclError or sysError:
            self.subset = error
        else:
            self.subset = result
        print "-"*100
        print result