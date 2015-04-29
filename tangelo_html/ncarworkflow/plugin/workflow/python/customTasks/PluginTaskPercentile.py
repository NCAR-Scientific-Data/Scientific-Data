import pyutilib.workflow
import rpy2.robjects as ro
import os
import tangelo

class PluginTaskPercentile(pyutilib.workflow.TaskPlugin):
    
    pyutilib.component.core.alias("taskPercentile")
    alias = "taskPercentile"
    
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('percentage')
        self.outputs.declare('result')

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
	#os.system("touch " + outfile)
        # Get path to the netcdf file
        #infile = self.filename
	infile = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/tmin_subset.nc"

	percent = self.percentage

        # Call the function that does the calculation
        ro.r['timePercentile'](infile, outfile, percent)

        self.result = "data/{0}/{1}_percentile.nc".format(wid,tid)
