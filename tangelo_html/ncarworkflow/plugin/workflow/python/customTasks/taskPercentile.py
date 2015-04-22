import pyutilib.workflow
import rpy2.robjects as ro
import os

class taskPercentile(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('percentile')
        self.outputs.declare('result')

    def execute(self):

	# Import the R script so we can use its function
        scriptname = "plugin/workflow/python/customTasks/r/r_calculation_module.R"
        ro.r['source'](scriptname)

        # Check if workflow directory exists, if not create one
        wid = "421"
        tid = "1040"

        workflowDirName = "/data/" + wid + "/"
        if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)

        # Uniquely name output file by task id
        outfile = workflowDirName + tid + "_percentile.nc"
        if os.path.exists(outfile): os.system("rm -rf " + outfile)

        # Get path to the netcdf file
        infile = self.filename

	# Get field based on file name
        field = infile.rsplit('_')[0]

        # Call the function that does the calculation
        ro.r['timePercentile'](infile, outfile, field, self.percentile)

        self.result = "data/{0}/{1}_percentile.nc".format(wid,tid)