"""@package docstring
This script subsets a NetCDF file via a NCL script. The NCL script subsets the NetCDF file by
a bounding rectangle given a Southwest Lat/Lon point and Northeast Lat/Lon point. It then creates
a new NetCDF file of the subsetted data
"""
import subprocess
import sys

def run(url, swlat, swlon, nelat, nelon, startyear, endyear):
    swLat = "swLat={}".format(swlat)
    swLon = "swLon={}".format(swlon)
    neLat = "neLat={}".format(nelat)
    neLon = "neLon={}".format(nelon)
    startYear = "startYear={}".format(startyear)
    endYear = "endYear={}".format(endyear)
    args = ['ncl' ,swLat, swLon, neLat, neLon, startYear, endYear, '../ncl/narccap_subset_tmin_time_latlon.ncl']
    status = subprocess.Popen(args)
    if status < 0:
        print "Error subsetting data"
	return { "alert": "Error subsetting data" }
    else:
      return { "subset": "tmin_subset_time_latlon.nc" }
