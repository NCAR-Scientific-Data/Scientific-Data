import subprocess
import sys

def run(filename,interval, method, outtime):
	status = subprocess.call(["ncl 'infile=\"{0}\"' 'outfile=\"tmin_aggregate_monthly.nc\"' 'varname=\"tmin\"' 'interval=\"{1}\"' 'methdod=\"{2}\"' 'outtime=\"{3}\"' aggregate.ncl".format(filename, interval, method, outtime)], shell=True)
      	if status < 0:
		print "Error aggregating data"
		return { "alert": "Error aggregating data" }
      	else:
       		return { "result":  "tmin_aggregate_monthly.nc" }

