import subprocess
import sys

def run(swlat, swlon, nelat, nelon, startyear, endyear):
    #return { "alert": "Inside Python" }
    print swlat, swlon, nelat, nelon, startyear, endyear
    status = subprocess.call(["ncl swLat={0} swLon={1} neLat={2} neLon={3} startYear={4} endYear={5} narccap_subset_tmin_time_latlon.ncl".format(swlat,swlon,nelat,nelon,startyear,endyear)], shell=True)
    if status < 0:
        print "Error subsetting data"
	return { "alert": "Error subsetting data" }
    else:
      status2 = subprocess.call(["ncl 'infile=\"tmin_subset_time_latlon.nc\"' 'outfile=\"tmin_aggregate_monthly.nc\"' 'varname=\"tmin\"' 'interval=\"month\"' aggregate.ncl"], shell=True)
      if status2 < 0:
	print "Error aggregating data"
	return { "alert": "Error aggregating data" }
      else:
	status3 = subprocess.call(["ncl 'filename=\"tmin_aggregate_monthly.nc\"' narccap_plot_tmin_latlon.ncl"], shell=True)
	if status3 < 0:
		print "Error plotting data"
		return { "alert": "Error plotting data" }
	return { "image": "tmin_latlon.png" }

