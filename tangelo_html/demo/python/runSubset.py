"""@package docstring
This script subsets a NetCDF file via a NCL script. The NCL script subsets the NetCDF file by
a bounding rectangle given a Southwest Lat/Lon point and Northeast Lat/Lon point. It then creates
a new NetCDF file of the subsetted data
"""
import subprocess
import sys

def run(url, swlat, swlon, nelat, nelon, startyear, endyear):
    status = subprocess.call(["ncl swLat={0} swLon={1} neLat={2} neLon={3} startYear={4} endYear={5} ncl/narccap_subset_tmin_time_latlon.ncl".format(swlat,swlon,nelat,nelon,startyear,endyear)], shell=True)
    if status < 0:
        print "Error subsetting data"
	return { "alert": "Error subsetting data" }
    else:
      return { "subset": "tmin_subset_time_latlon.nc" }
