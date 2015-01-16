import subprocess
import sys

def runNCL():
    status = subprocess.call(["ncl narccap_subset_tmin_time_latlon.ncl"], shell=True)
    if status < 0:
        print "Error subsetting data"
    else:
      status2 = subprocess.call(["ncl 'infile=\"tmin_subset_time_latlon.nc\"' 'outfile=\"tmin_aggregate_monthly.nc\"' 'varname=\"tmin\"' 'interval=\"month\"' aggregate.ncl"], shell=True)
      if status2 < 0:
	print "Error aggregating data"
      else:
	status3 = subprocess.call(["ncl 'filename=\"tmin_aggregate_monthly.nc\"' narccap_plot_tmin_latlon.ncl"], shell=True)
	if status3 < 0:
	   print "Error plotting data"

if __name__ == "__main__":
    runNCL()
