"""@package docstring
This script Aggregates data in from a given NetCDF file via a NCL script. The NCL script
takes in an input file, output file, the variable on which to aggregate, the method to use (mean, min, max),
the interval on which to aggregate (day, month, season, or year), and the outtime to set (the date/time of interval
to set the aggregate result). The output file is then a NetCDF with the aggregate data
"""

import subprocess
import sys
import re
import pyutilib.workflow
import os

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
            wid = "wid={0}".format(self.workflowID)
            tid = "tid={0}".format(self.id)
            
            args = ['ncl', '-n', '-Q', wid, tid, sFilename, sVariable, sOutunit, 'ncl/unit_conversion.ncl']
            args = filter(None,args)

            sysError = False
            nclError = False
            try:
                    status = subprocess.check_call(args)
            except:
                    sysError = True
                    error = "System Error: Please contact site administrator."
        
            nclError = False
            result = "/data/{0}/{1}_unitconv.nc".format(self.workflowID,self.id)
            if not sysError:
                if not os.path.isfile(result):
                    error = "NCL Error: Please check input parameters."
                    nclError = True
            if nclError or sysError:
                    self.result = error 
            else:
                    self.result = result