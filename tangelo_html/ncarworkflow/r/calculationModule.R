##########################################################
#
#    Name:    calculationModule.R
#    Summary: This scripts are a collection of R functions
#			   that does some data analysis operations
#
##########################################################

##########################################################
#
#    Name:    daysWithinThreshold
#    Summary: Calculate number of days that
#             a specific field is within a specific range.
#             Now this script only takes days as frequency
#             and it only works with daily data for proof-of-concept.
#
#    Parameters: Subset file name, the field needs to be calculated
#                Lower limit of the threshold, upper limit of the threshold
#				 output file name
#
##########################################################
daysWithinThreshold <- function(filename, field, lower, upper, outputFname){
	# Import required libraries
	library(ncdf)

	# Open the NetCDF file
	nc = open.ncdf(filename)

	# Read the field data and its dimension off the NetCDF file
	field_data = get.var.ncdf(nc, field)
	field_dimsize = length(dim(field_data))

	# Read off the time dimension
	time = nc$dim$time$vals

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
	climatology <- apply(field_data, c(field_dimsize), function(x){sum(x>=lower & x <=upper)})

	# Subset the field, time variables and then output to a new netcdf file
	index = which(climatology != 0)
	time_sub <- time[index]
	field_sub <- subset(field_data, time %in% time_sub, drop=FALSE)

	# After subset() the field lost all the dimensions, need to change
	# the subset back to its old dimension
	field_sub_dim = dim(field_data)
	field_sub_dim[field_dimsize] = length(time_sub)
	dim(field_sub) <- field_sub_dim

	# Open the output NetCDF file and then write the subsets to a new netcdf file
	nc_out = open.ncdf(outputFname, write=TRUE)
	put.var.ncdf(nc_out, field, field_sub)
	put.var.ncdf(nc_out, "time", time_sub)
}

##########################################################
#
#    Name:    ncdfDelta
#    Summary: Calculates delta between two subsets and output
#				to a new NetCDF file
#
#    Parameters: Name of first file name, name of second file name
#					name of the output file, filed to be calculatedS
#
##########################################################
ncdfDelta <- function(filename1, filename2, outputFname, field){
	library(ncdf)	

	nc1 = open.ncdf(filename1)
	field1 = get.var.ncdf(nc1, field)

	nc2 = open.ncdf(filename2)
	field2 = get.var.ncdf(nc2, field)

	field_delta = abs(field1 - field2)

	nc3 = open.ncdf(outputFname, write=TRUE)
	put.var.ncdf(nc3, field, field_delta)
}
