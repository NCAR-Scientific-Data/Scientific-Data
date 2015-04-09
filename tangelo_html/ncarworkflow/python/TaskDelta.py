import pyutilib.workflow
import rpy2.robjects as ro
import os

class taskDelta(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename1')
        self.inputs.declare('filename2')
        self.inputs.declare('outputfname')
        self.inputs.declare('field')

    def execute(self):
	
	# Check if workflow directory exists, if not create one
	wid = self.workflowID
	tid = self.id
	
	workflowDirName = "/data/" + wid + "/" 
	if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)
	
	# Uniquely name output file by task id
	outputFname = workflowDirName + tid + "_delta.nc"
	if os.path.exists(outputFname): os.system("rm -rf " + outputFname)

	# Calculate delta using R script
	scriptName = "/home/project/Scientiic-Data/tangelo_html/ncarworkflow/r/calculationModule.R"
	ro.r['source'](scriptName)

	# Check if workflow directory exists, if not create one
	#Create a output file by copyinh the first file since
	#    R is inefficient when output to new NetCDF file
	command = "cp " + self.filename1 + " " + outputFname
	os.system(command)

	# Call the function that does the calculation
	ro.r['ncdfDelta'](self.filename1, self.filename2, outputFname, self.field)
