"""@package docstring
This script subsets a NetCDF file via a NCL script. The NCL script subsets the NetCDF file by
a bounding rectangle given a Southwest Lat/Lon point and Northeast Lat/Lon point. It then creates
a new NetCDF file of the subsetted data
"""
import subprocess
import sys
import re
import pyutilib.workflow

class TaskSubset(pyutilib.workflow.Task):
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
        startDate = "startDate={0}".format(self.startdate)
        endDate = "endDate={0}".format(self.enddate)
        filename = "filename=\"{0}\"".format(self.url)
        v = "variable=\"{0}\"".format(self.variable)
        wid = "wid={0}".format(self.workflowid)
        tid = "tid={0}".format(self.id)
        
        args = ['ncl', '-n', '-Q', wid, tid, filename, v, swLat, swLon, neLat, neLon, startDate, endDate, 'ncl/narccap_subset_tmin_time_latlon.ncl']
        sysError = False
        nclError = False
        try:
            status = subprocess.Popen(args,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            sysError = True
            error = "System error, please contact the site administrator"

        if not sysError:
            for line in status.stdout:
                if line.find("fatal") != -1:
                    nclError = True
                    error = re.sub('\[.*?\]:',' ',line)
                    break
        result = "/data/{0}/{1}_subset.nc".format(wid,tid)
        if nclError or sysError:
            self.subset = { "error": error }
        else:
            self.subset = { "subset": result }