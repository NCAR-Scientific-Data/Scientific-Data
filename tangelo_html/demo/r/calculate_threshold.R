##########################################################
#
#    Name:    calculate_threshold.R
#    Summary: This scripts calculate number of days that
#             a specific field is within a specific range.
#             Now this script only takes days as frequency
#             and it only works with daily data for proof-of-concept.
#
#    Parameters: Subset file name, the field needs to be calculated
#                Lower limit of the threshold, upper limit of the threshold
#
##########################################################
rfunc <- function(filename, field, lower, upper){
	# Import required libraries
	library(ncdf)

	# Open the NetCDF file
	nc = open.ncdf(filename)

	# Read the field data off the NetCDF file
	field_data = get.var.ncdf(nc, field)	
	
	# If user didn't specify a lower limit or upper limit
	#     then set the lower limit to min or set the upper limit to max
	if (lower == "min") {
        	lower = min(field_data)
	} else {
        	lower = as.numeric(lower)
	}

	if (upper == "max") {
        	upper = max(field_data)
	} else {
        	upper = as.numeric(upper)
	}
	
	# Calculate the number of days that the field within a threshold
	#    First apply the threshold to the field, it will returns an array
	#    with length equals to length of the time variable. Value in
	#    each elements represents number of values that within a threshold
	#    in that time, if the value is 0, it means on that day the field is
	#    not in the threshold, if the value is > 0, it means that day is
	#    with in the threshold.
	#
	#    Then get the number of the elements has value of 0, subtract that number
	#    from the total number of days to get the final result.
	climatology <- apply(field_data, c(length(dim(field_data))), function(x){sum(x>=lower & x <=upper)})
	time <- nc$dim$tim$vals
	totalDays <- dim(time)
	numDaysWithinThreshold <- totalDays - sum(climatology == 0)
	return(numDaysWithinThreshold)
}
