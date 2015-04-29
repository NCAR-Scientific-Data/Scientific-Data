#    File: PluginTaskClimatology.py
#    This script calculates average for a specific range in a year
#    for multiple years from a given NetCDF file via a R script
#    takes in an input file, output file, the variable on which to average.
#    The output file is then a NetCDF with the average data
import pyutilib.workflow
import rpy2.robjects as ro
import os

#    Class: taskClimatology
#    A task class that average data
#
#    Attributes:
#
#    infile - the name of the NetCDF file to average
#    startmonth - the start month of the range
#    endmonth - the end month of the range
#    result - the resulting output
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
        scriptname = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/plugin/workflow/python/customTasks/r/r_calculation_module.R"
        ro.r['source'](scriptname)

        # Check if workflow directory exists, if not create one
        wid = "filename=\"{0}\"".format(self.workflowID)
        tid = "filename=\"{0}\"".format(self.uid)

        workflowDirName = "/home/project/Scientific-Data/tangelo_html/ncarworkflow/python/data/" + wid + "/"
        if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)

        # Uniquely name output file by task id
        outfile = workflowDirName + tid + "_climatology.nc"
        if os.path.exists(outfile): os.system("rm -rf " + outfile)

        # Get path to the netcdf file
        infile = self.filename
        start = self.startmonth
        end = self.endmonth

        # Get field based on file name
        #field = infile.rsplit('_')[0]

        # Call the function that does the calculation
        ro.r['calculateClimatology'](infile, outfile, start, end, field)

        self.result = "data/{0}/{1}_climatology.nc".format(wid,tid)
