"""@package docstring
This script plots a given NetCDF file and returns a .png of the plot via a NCL script. The NCL script
simply takes in a NetCDF file and returns a plot using a standard projection.
"""

import subprocess
import sys
import re

def run(filename, timeindex, native):
        sFilename = "filename=\"{0}\"".format(filename)
        if not timeindex:
                sTimeindex = "timeindex=0"
        else:
                sTimeindex = "timeindex={0}".format(timeindex)
        sOutfile = "outfile=\"tmin_latlon\""
        if native:
                plotScript = 'ncl/narccap_plot_tmin_native.ncl'
        else:
                plotScript = 'ncl/narccap_plot_tmin_latlon.ncl'
        args = ['ncl', sFilename, sTimeindex, sOutfile, plotScript]
        sysError = False
        try:
                status = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	except OSError as e:
                print "Error: {0}".format(e.strerror)
                sysError = True
                raise
        except ValueError as e:
                print "Error: Invalid argument to Popen."
                sysError = True
                raise
        except:
                print "Unknown error."
                sysError = True
                raise
    
        isError = False
        error = ''
        if not sysError:
                for line in status.stdout:
                        if line.find("fatal") != -1:
                            isError = True
                            error = re.sub('\[.*?\]:',' ',line)
                            break
                        if line.find("Invalid") != -1:
                            isError = True
                            error = re.sub('.*?Invalid','Invalid',line)
                            break
        if isError:
                return { "error": error }
        else:
		return { "image": "tmin_latlon.png" }

