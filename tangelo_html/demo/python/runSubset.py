"""@package docstring
This script subsets a NetCDF file via a NCL script. The NCL script subsets the NetCDF file by
a bounding rectangle given a Southwest Lat/Lon point and Northeast Lat/Lon point. It then creates
a new NetCDF file of the subsetted data
"""
import subprocess
import sys

def run(url, swlat, swlon, nelat, nelon, startyear, endyear):
    swLat = "swLat={0}".format(swlat)
    swLon = "swLon={0}".format(swlon)
    neLat = "neLat={0}".format(nelat)
    neLon = "neLon={0}".format(nelon)
    startYear = "startYear={0}".format(startyear)
    endYear = "endYear={0}".format(endyear)
    filename = "filename=\"../tmin.CRCM.ncep.dayavg.native.nc\""
    args = ['ncl', filename, swLat, swLon, neLat, neLon, startYear, endYear, '../ncl/narccap_subset_tmin_time_latlon.ncl']
    status = subprocess.call(args)
    if status < 0:
        print "Error subsetting data"
	return { "alert": "Error subsetting data" }
    else:
      return { "subset": "tmin_subset_time_latlon.nc" }
