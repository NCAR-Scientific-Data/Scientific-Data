"""@package docstring
This script plots a given NetCDF file and returns a .png of the plot via a NCL script. The NCL script
simply takes in a NetCDF file and returns a plot using a standard projection.
"""

import subprocess
import sys
import re
import pyutilib.workflow

class RunPlot(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('filename')
        self.inputs.declare('timeindex')
        self.inputs.declare('native')
        self.outputs.declare('result')
        
    def execute(self):
        sFilename = "filename=\"{0}\"".format(self.filename)
        if not self.timeindex:
                sTimeindex = "timeindex=0"
        else:
                sTimeindex = "timeindex={0}".format(self.timeindex)
        sOutfile = "outfile=\"tmin_latlon\""
        if self.native:
                plotScript = 'ncl/narccap_plot_tmin_native.ncl'
        else:
                plotScript = 'ncl/narccap_plot_tmin_latlon.ncl'
        args = ['ncl', '-n', sFilename, sTimeindex, sOutfile, plotScript]
        sysError = False
        nclError = False
        try:
                status = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        except:
                sysError = True
                error = "System error, please contact site administrator."
    
        if not sysError:
                for line in status.stdout:
                        if line.find("fatal") != -1:
                            nclError = True
                            error = re.sub('\[.*?\]:',' ',line)
                            break
                        if line.find("Invalid") != -1:
                            nclError = True
                            error = re.sub('.*?Invalid','Invalid',line)
                            break
        if nclError or sysError:
                self.result = { "error": error }
        else:
                self.result = { "image": "tmin_latlon.png" }