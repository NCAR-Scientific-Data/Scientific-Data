import subprocess
import sys

def run(swlat, swlon, nelat, nelon, startyear, endyear):
    status = subprocess.call(["ncl swLat={0} swLon={1} neLat={2} neLon={3} startYear={4} endYear={5} narccap_subset_tmin_time_latlon.ncl".format(swlat,swlon,nelat,nelon,startyear,endyear)], shell=True)
    if status < 0:
        print "Error subsetting data"
	return { "alert": "Error subsetting data" }
    else:
      return { "subset": "tmin_subset_time_latlon.nc" }
