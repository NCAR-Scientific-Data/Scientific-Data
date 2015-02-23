"""@package docstring
This script subsets a NetCDF file via a NCL script. The NCL script subsets the NetCDF file by
a bounding rectangle given a Southwest Lat/Lon point and Northeast Lat/Lon point. It then creates
a new NetCDF file of the subsetted data
"""
import subprocess
import sys
import re

def run(url, variable, swlat, swlon, nelat, nelon, startdate, enddate):
    swLat = "swLat={0}".format(swlat)
    swLon = "swLon={0}".format(swlon)
    neLat = "neLat={0}".format(nelat)
    neLon = "neLon={0}".format(nelon)
    startDate = "startDate={0}".format(startdate)
    endDate = "endDate={0}".format(enddate)
    filename = "filename=\"{0}\"".format(url)
    v = "variable=\"{0}\"".format(variable)
    
    args = ['ncl', filename, v, swLat, swLon, neLat, neLon, startDate, endDate, 'ncl/narccap_subset_tmin_time_latlon.ncl']
    sysError = False
    try:
        status = subprocess.Popen(args,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
    if isError:
        return { "error": error }
    else:
        return { "subset": "tmin_subset_time_latlon.nc" }
