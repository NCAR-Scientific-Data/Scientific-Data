import pyutilib.workflow
import rpy2.robjects as ro
import os
import tangelo

#   Class: PluginTaskDelta
#   A task that calculate the delta between two subsets.
#
#   Attributes:
#
#           filename1 - The name of the first NetCDF file.
#           filename2 - The name of the second NetCDF file.
class PluginTaskDelta(pyutilib.workflow.TaskPlugin):
    
    pyutilib.component.core.alias("taskDelta")
    alias = "taskDelta"
    #   Constructor: __init__
    #   Creates a Delta task
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #       *args - A list of arguments.
    #       **kwds - A list of keyword arguments.
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename1')
        self.inputs.declare('filename2')
	    self.outputs.declare('result')

    #   Function: execute
    #   Calls the R function to calculate the delta of the two files.
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #
    #   Returns:
    #
    #       The path of the resulting file containing the delta values.
    def execute(self):

        infile1 = self.filename1
        infile2 = self.filename2

        # Check if workflow directory exists, if not create one
        wid = self.workflowID
        tid = self.uid

        workflowDirName = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/python/data/" + wid + "/"
        if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)

        # Uniquely name output file by task id
        outfile = workflowDirName + tid + "_delta.nc"
        if os.path.exists(outfile): os.system("rm -rf " + outfile)
        os.system("touch " + outfile)

        # Calculate delta using R script
        scriptName = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/plugin/workflow/python/customTasks/r/r_calculation_module.R"
        ro.r['source'](scriptName)

        # Check if workflow directory exists, if not create one
        # Create a output file by copying the first file 
        command = "cp " + infile1 + " " + outfile
        os.system(command)

        # Call the function that does the calculation
        ro.r['ncdfDelta'](infile1, infile2, outfile)
        self.result = "/data/{0}/{1}_delta.nc".format(wid,tid)
