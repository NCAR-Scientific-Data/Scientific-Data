"""@package docstring
This script plots a given NetCDF file and returns a .png of the plot via a NCL script. The NCL script
simply takes in a NetCDF file and returns a plot using a standard projection.
"""

import subprocess
import sys

def run(filename, timeindex, native):
        sFilename = "filename=\"{0}\"".format(filename)
        sTimeindex = "timeindex={0}".format(timeindex)
        sOutfile = "outfile=\"tmin_latlon\""
        if native:
                plotScript = 'ncl/narccap_plot_tmin_native.ncl'
        else:
                plotScript = 'ncl/narccap_plot_tmin_latlon.ncl'
        args = ['ncl', sFilename, sTimeindex, sOutfile, plotScript]
	status = subprocess.call(args)
	if status < 0:
		print "Error plotting data"
		return { "alert": "Error plotting data" }
        else:
		return { "image": "tmin_latlon.png" }

