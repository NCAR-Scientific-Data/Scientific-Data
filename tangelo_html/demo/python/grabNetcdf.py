"""@package docstring
This script uses inputs from index.html to pull a netCDF file from the server.
NARCCAP OPeNDAP url convention:
	narrcap.regional-climate-model.global-climate-model.table.variable.version.aggregation
	narccap.regional-climate-model.ncep.table.variable.version.aggregation
Parameters:
	simulationType: This is either ncep, -current, or -future.
	variable: Any variable from tables 1, 2, or 3.
	swlat: the southwest latitude boundary.
	swlon: the southwest longitude boundary.
	nelat: the northeast latitude boundary.
	nelon: the northeast longitude boundary.
	timeStart: the beginning time range, in format YYYY-MM-DD
	timeEnd: the ending time block, in format YYYY-MM-DD
	rcm: the regional climate model.
	gcm: the global climate model ('none' if ncep is selected) 
"""
import runSubset
import urlCatalog

def run(simulationType="", variable="", swlat="", swlon="", nelat="", nelon="", timeStart="", timeEnd="", rcm="", gcm=""):
	basicString = "http://tds.ucar.edu/thredds/dodsC/narccap."
	modelString = rcm + "." + gcm + simulationType + "." + variable[:6]
	version = urlCatalog.urlCatalog[modelString]
	modelString += variable[6:]
	
	if version == 0:
		version = ".aggregation"
	else:
		version = "." + str(version) + ".aggregation"
	
	url = basicString + modelString + version
	timeStart = "\"{0}\"".format(timeStart)
	timeEnd = "\"{0}\"".format(timeEnd)
	
	return runSubset.run(url, variable[7:], swlat, swlon, nelat, nelon, timeStart, timeEnd)
