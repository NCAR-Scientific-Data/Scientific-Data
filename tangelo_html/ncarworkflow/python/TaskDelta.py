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
	
	#Create a output file by copyinh the first file since
	#    R is inefficient when output to new NetCDF file
	command = "cp " + self.filename1 + " " + self.outputfname
	os.system(command)

	# Calculate delta using R script
	scriptName = "ncarworkflow/r/calculationModule.R"
	ro.r['source'](scriptName)

	# Call the function that does the calculation
	ro.r['ncdfDelta'](self.filename1, self.filename2, self.outputfname, self.field)
