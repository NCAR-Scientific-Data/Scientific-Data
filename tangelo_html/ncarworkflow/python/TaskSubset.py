"""@package docstring
This script subsets a NetCDF file via a NCL script. The NCL script subsets the NetCDF file by
a bounding rectangle given a Southwest Lat/Lon point and Northeast Lat/Lon point. It then creates
a new NetCDF file of the subsetted data
"""
import subprocess
import sys
import re
import pyutilib.workflow
import os

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
        wid = "wid={0}".format(self.workflowID)
        tid = "tid={0}".format(self.id)
        
        args = ['ncl', '-n', '-Q', filename, v, swLat, swLon, neLat, neLon, startDate, endDate, wid, tid, 'ncl/subset_time_latlon.ncl']
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
        result = "/data/{0}/{1}_subset.nc".format(self.workflowID, self.id)
        if not sysError or not nclError:
            if not os.path.isfile(result):
                error = "NCL Error: Error with NCL script"
                nclError = True
        if nclError or sysError:
            self.subset = error
        else:
            self.subset = result