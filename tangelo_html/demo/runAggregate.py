"""@package docstring
This script Aggregates data in from a given NetCDF file via a NCL script. The NCL script
takes in an input file, output file, the variable on which to aggregate, the method to use (mean, min, max),
the interval on which to aggregate (day, month, season, or year), and the outtime to set (the date/time of interval
to set the aggregate result). The output file is then a NetCDF with the aggregate data
"""

import subprocess
import sys

def run(filename,interval, method, outtime):
	status = subprocess.call(["ncl 'infile=\"{0}\"' 'outfile=\"tmin_aggregate_monthly.nc\"' 'varname=\"tmin\"' 'interval=\"{1}\"' 'method=\"{2}\"' 'outtime=\"{3}\"' aggregate.ncl".format(filename, interval, method, outtime)], shell=True)
      	if status < 0:
		print "Error aggregating data"
		return { "alert": "Error aggregating data" }
      	else:
       		return { "result":  "tmin_aggregate_monthly.nc" }

