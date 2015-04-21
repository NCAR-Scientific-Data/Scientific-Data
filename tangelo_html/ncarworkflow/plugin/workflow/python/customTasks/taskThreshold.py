import pyutilib.workflow
import rpy2.robjects as ro
import os

class taskThreshold(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('lower')
        self.inputs.declare('upper')
        self.outputs.declare('result')

    def execute(self):

	# Import the R script so we can use its function
        scriptname = "plugin/workflow/python/customTasks/r/r_calculation_module.R"
        ro.r['source'](scriptname)

        # Check if workflow directory exists, if not create one
        wid = str(421)
        tid = str(100)

        workflowDirName = "/data/" + wid + "/"
        if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)

        # Uniquely name output file by task id
        outputFname = workflowDirName + tid + "_threshold.nc"
        if os.path.exists(outputFname): os.system("rm -rf " + outputFname)

        # Get field based on file name
        field = self.filename.rsplit('_')[0]
	print "field is: " + field
        # Check if user entered lowerlimit and upperlimit, if not
        #   Set lower to min or upper to max
        lowerlimit = str(self.lower) if self.lower else "min"
        upperlimit = str(self.upper) if self.upper else "max"

        # Get path to the netcdf file
        fname = "/data/" + self.filename

        # R is inefficient when output to new NetCDF file
        command = "cp " + fname + " " + outputFname
        os.system(command)

        # Call the function that does the calculation
        value = ro.r['daysWithinThreshold'](fname, field, lowerlimit, upperlimit, outputFname)

        self.result = "data/{0}/{1}_threshold.nc".format(wid,tid)
	print "value is: " + str(value)
