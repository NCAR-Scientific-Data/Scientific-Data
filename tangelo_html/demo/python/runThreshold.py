import subprocess
import sys
import re
import rpy2.robjects as ro

def run(filename, field, lower, upper):
	# Check if user entered lowerlimit and upperlimit, if not
	#	Set lower to min or upper to max
        lowerlimit = str(lower) if lower else "min"
	upperlimit = str(upper) if upper else "max"

	# Import the R script so we can use its function
	scriptname = "../r/calculate_threshold.R"
	ro.r['source'](scriptname)

	# Call the function that does the calculation
	value = ro.r['rfunc'](filename, field, lowerlimit, upperlimit)
