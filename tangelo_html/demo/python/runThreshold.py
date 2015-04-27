"""@package docstring
This script calculates number of days a specfic scientific data field(Tempature, wind speed, etc..) is within a specfic range from a given NetCDF file via a R script. The R script takes in an input file, a climate data field, a lower limit and an upper limit of the range of the field. The output is a numeric value represents number of days.
"""

import rpy2.robjects as ro

def run(filename, field, lower, upper):
	# Check if user entered lowerlimit and upperlimit, if not
	#	Set lower to min or upper to max
        lowerlimit = str(lower) if lower else "min"
	upperlimit = str(upper) if upper else "max"

	# Import the R script so we can use its function
	scriptname = "r/calculate_threshold.R"
	ro.r['source'](scriptname)

	# Call the function that does the calculation
	value = ro.r['rfunc'](filename, field, lowerlimit, upperlimit)
	print value
