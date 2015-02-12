"""@package docstring
This script uses inputs from index.html to pull a netCDF file from the server.
NARCCAP OPeNDAP url convention:
	narrcap.regional-climate-model.global-climate-model.table.variable.version.aggregation
	narccap.regional-climate-model.ncep.table.variable.version.aggregation
Parameters:
	simulation_type: This is either ncep, -current, or -future.
	variable: Any variable from tables 1, 2, or 3.
	swLat: the southwest latitude boundary.
	swLon: the southwest longitude boundary.
	neLat: the northeast latitude boundary.
	neLon: the northeast longitude boundary.
	timestart: the beginning time range, in format YYYY-MM-DD
	timeend: the ending time block, in format YYYY-MM-DD
	rcm: the regional climate model.
	gcm: the global climate model ('none' if ncep is selected) 
"""
import runSubset
import urlCatalog

def run(simulation_type="", variable="", swLat="", swLon="", neLat="", neLon="", timestart="", timeend="", rcm="", gcm=""):
	basicString = "http://tds.ucar.edu/thredds/dodsC/narccap."
	modelString = rcm + "." + gcm + simulation_type + "." + variable[:6]
	version = urlCatalog.urlCatalog[modelString]
	if version == 0:
		version = ".aggregation"
	else:
		version = "." + str(version) + ".aggregation"
	url = basicString + modelString + version
	return runSubset.run(url, swLat, swLon, neLat, neLon, timestart, timeend)
