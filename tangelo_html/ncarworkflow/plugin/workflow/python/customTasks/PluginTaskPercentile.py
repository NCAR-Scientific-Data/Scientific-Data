import pyutilib.workflow
import rpy2.robjects as ro
import os
import tangelo

#   Class: PluginTaskPercentile
#   A task class that calculates Percentile.
#
#   Attributes:
#   
#       filename - The name of the NetCDF file to perform calculations on.
#       percentage - The percentage to calculate percentile for.
#       result - The resulting output.
class PluginTaskPercentile(pyutilib.workflow.TaskPlugin):
    
    pyutilib.component.core.alias("taskPercentile")
    alias = "taskPercentile"
    
    #   Constructor: __init__
    #   Creates a Percentile task.
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #       *args - A list of arguments.
    #       **kwds - A list of keyword arguments.
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('percentage')
        self.outputs.declare('result')

    #   Function: execute
    #   Calls the r function to calculate percentile.
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #
    #    Returns:
    #
    #       The result.
    def execute(self):

	# Import the R script so we can use its function
        scriptname = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/plugin/workflow/python/customTasks/r/r_calculation_module.R"
        ro.r['source'](scriptname)

        # Check if workflow directory exists, if not create one
        wid = self.workflowID
        tid = self.uid

        workflowDirName = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/python/data/" + wid + "/"
        if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)

        # Uniquely name output file by task id
        outfile = workflowDirName + tid + "_percentile.nc"
        if os.path.exists(outfile): os.system("rm -rf " + outfile)

        # Get path to the netcdf file
        infile = self.filename

	    percent = self.percentage

        # Call the function that does the calculation
        ro.r['timePercentile'](infile, outfile, percent)

        self.result = "data/{0}/{1}_percentile.nc".format(wid,tid)
