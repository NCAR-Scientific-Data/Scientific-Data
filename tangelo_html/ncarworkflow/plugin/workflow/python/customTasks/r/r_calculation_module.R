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
daysWithinThreshold <- function(infile, outfile, field, lower, upper){
	# Import required libraries
	library(ncdf)

	# Open the NetCDF file
	nc = open.ncdf(infile)

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
	field_sub <- field_data[,,index]

	# Calculate number of days
	n_step = length(time_sub)

	# Copy input file to output file
	from = 0
	to = n_step - 1
	dimension = gsub(" ", "", paste("time",",",from,",",to))
	command = paste("ncks -d ",dimension,infile,outfile)
	system(command)

	# Open the output NetCDF file and then write the subsets to a new netcdf file
	nc_out = open.ncdf(outfile, write=TRUE)
	
	put.var.ncdf(nc_out, "time", time_sub)
	put.var.ncdf(nc_out, field, field_sub)
	close.ncdf(nc_out)
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
timePercentile <- function(inputfname, outputfname, field, percentile){
	library(ncdf)	

	nc = open.ncdf(inputfname)

	field_data = get.var.ncdf(nc, field)

	time_data = nc$dim$time$vals

	percentage = percentile/100

	time_sub_close = quantile(time, probs=c(percentage))

	time_sub = which.min(abs(time - time_sub))+ min(time)

	index = which(time == time_sub)

	tmin_sub = tmin[,,index]
}
