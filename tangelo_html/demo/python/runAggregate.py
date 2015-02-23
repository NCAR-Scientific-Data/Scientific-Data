"""@package docstring
This script Aggregates data in from a given NetCDF file via a NCL script. The NCL script
takes in an input file, output file, the variable on which to aggregate, the method to use (mean, min, max),
the interval on which to aggregate (day, month, season, or year), and the outtime to set (the date/time of interval
to set the aggregate result). The output file is then a NetCDF with the aggregate data
"""

import subprocess
import sys
import re

def run(filename, interval, method, outtime):
        infile = "infile=\"{0}\"".format(filename)
        sInterval = "interval=\"{0}\"".format(interval)
        if not method:
                sMethod = ""
        else:
                sMethod = "method=\"{0}\"".format(method)
        if not outtime:
                sOuttime = ""
        else:
                sOuttime = "outtime=\"{0}\"".format(outtime)
        outfile = "outfile=\"tmin_aggregate_monthly.nc\""
        varname = "varname=\"tmin\""
        args = ['ncl', infile, outfile, varname, sInterval, sMethod, sOuttime, 'ncl/aggregate.ncl']
        args = filter(None,args)

        sysError = False
        try:
                status = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
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
                        if line.find("Invalid") != -1:
                            isError = True
                            error = re.sub('.*?Invalid','Invalid',line)
                            break
        if isError:
                return { "error": error }
        else:
                return { "result":  "tmin_aggregate_monthly.nc" }

