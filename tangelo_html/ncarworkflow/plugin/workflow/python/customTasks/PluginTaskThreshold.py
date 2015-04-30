import pyutilib.workflow
import uuid
import rpy2.robjects as ro
import os
import tangelo

#   Class: PluginTaskThreshold
#   A task class that filters data by a threshold.
#
#   Attributes:
#   
#       filename - The name of the NetCDF file to aggregate.
#       lower - The lower bounds of the threshold
#       upper - The uppoer bounds of the threshold
#       result - The resulting output.
class PluginTaskThreshold(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskThreshold")
    alias="taskThreshold"

    #   Constructor: __init__
    #   Creates a threshold task.
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
        self.inputs.declare('lower')
        self.inputs.declare('upper')
        self.outputs.declare('result')

    #   Function: execute
    #   Calls the r function to threshold the data.
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
        tid = self.id

        workflowDirName = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/python/data/" + str(wid) + "/"
        if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)

        # Get path to the netcdf file
        infile = self.filename

       # Uniquely name output file by task id
        outfile = workflowDirName + str(tid) + "_threshold.nc"
        if os.path.exists(outfile): os.system("rm " + outfile)

        # Check if user entered lowerlimit and upperlimit, if not
        #   Set lower to min or upper to max
        low = self.lower
        up = self.upper
        lowerlimit = str(low) if self.lower else "min"
        upperlimit = str(up) if self.upper else "max"

        # Call the function that does the calculation
        ro.r['daysWithinThreshold'](infile, outfile, lowerlimit, upperlimit)

        self.result = "data/{0}/{1}_threshold.nc".format(wid,tid)
