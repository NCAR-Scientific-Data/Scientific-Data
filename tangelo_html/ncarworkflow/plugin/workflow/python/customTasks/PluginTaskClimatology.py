import pyutilib.workflow
import rpy2.robjects as ro
import os

class PluginTaskClimatology(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskClimatology")
    alias = "taskClimatology"

    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('startmonth')
        self.inputs.declare('endmonth')
        self.outputs.declare('result')

    def execute(self):
        
        # Import the R script so we can use its function
        scriptname = "plugin/workflow/python/customTasks/r/r_calculation_module.R"
        ro.r['source'](scriptname)

        # Check if workflow directory exists, if not create one
        wid = "filename=\"{0}\"".format(self.workflowID)
        tid = "filename=\"{0}\"".format(self.uid)

        workflowDirName = "/data/" + wid + "/"
        if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)

        # Uniquely name output file by task id
        outfile = workflowDirName + tid + "_climatology.nc"
        if os.path.exists(outfile): os.system("rm -rf " + outfile)

        # Get path to the netcdf file
        infile = "filename=\"{0}\"".format(self.filename)
        start = "filename=\"{0}\"".format(self.startmonth)
        end = "filename=\"{0}\"".format(self.endmonth)

        # Get field based on file name
        field = infile.rsplit('_')[0]

        # Call the function that does the calculation
        ro.r['calculateClimatology'](infile, outfile, start, end, field)

        self.result = "data/{0}/{1}_climatology.nc".format(wid,tid)
