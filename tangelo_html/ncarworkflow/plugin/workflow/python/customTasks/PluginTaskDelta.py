import pyutilib.workflow
import rpy2.robjects as ro
import os
import tangelo

#   Class: taskDelta
#   Task that calculate the delta between two subsets
class PluginTaskDelta(pyutilib.workflow.TaskPlugin):
    
    pyutilib.component.core.alias("taskDelta")
    alias = "taskDelta"

    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename1')
        self.inputs.declare('filename2')
	self.outputs.declare('result')
    def execute(self):

	infile1 = "filename=\"{0}\"".format(self.filename1) 
	infile2 = "filename=\"{0}\"".format(self.filename2)

    	# Check if workflow directory exists, if not create one
    	wid = "filename=\"{0}\"".format(self.workflowID)
    	tid = "filename=\"{0}\"".format(self.uid)

    	workflowDirName = "/data/" + wid + "/"
    	if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)

    	# Uniquely name output file by task id
    	outfile = workflowDirName + tid + "_delta.nc"
    	if os.path.exists(outfile): os.system("rm -rf " + outfile)

    	# Calculate delta using R script
    	scriptName = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/plugin/workflow/python/customTasks/r/r_calculation_module.R"
    	ro.r['source'](scriptName)

    	# Check if workflow directory exists, if not create one
    	# Create a output file by copying the first file 
    	command = "cp " + infile1 + " " + outfile
    	os.system(command)

	# Get field based on file name
        field = infile1.rsplit('_')[0]

    	# Call the function that does the calculation
    	ro.r['ncdfDelta'](infile1, infile2, outfile, field)
    	self.result = "/data/{0}/{1}_delta.nc".format(wid,tid)
