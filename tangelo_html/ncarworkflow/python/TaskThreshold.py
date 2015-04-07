import pyutilib.workflow
import rpy2.robjects as ro

class taskThreshold(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('field')
        self.inputs.declare('lower')
        self.inputs.declare('upper')

    def execute(self):
	# Check if user entered lowerlimit and upperlimit, if not
	#	Set lower to min or upper to max
        lowerlimit = str(self.lower) if self.lower else "min"
	upperlimit = str(self.upper) if self.upper else "max"

	# Import the R script so we can use its function
	scriptname = "tangelo_html/demo/r/calculate_threshold.R"
	ro.r['source'](scriptname)

	# Call the function that does the calculation
	value = ro.r['rfunc'](self.filename, self.field, lowerlimit, upperlimit)
