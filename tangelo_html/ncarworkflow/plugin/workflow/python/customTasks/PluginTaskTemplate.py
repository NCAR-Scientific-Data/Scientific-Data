import subprocess
import pyutilib.workflow
import os
import tangelo

"""
  Class: PluginTaskTemplate
  A template for implementing new workflow tasks
"""

class PluginTaskTemplate(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskTemplate")
    alias = "taskTemplate"
    
    """
       Constructor: __init__
       Creates a Template Task
    
       Parameters:
    
           self - A reference to the object.
           *args - A list of arguments
           **kwds - A list of keyword arguments.
    """

    def __init__(self,*args,**kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('input1')
        self.inputs.declare('input2')
        self.outputs.declare('output1')

    """
       Function: execute
       Calls an analysis script to process data
    
       Parameters:
    
           self - A reference to the object.
    
        Returns:
    
           The path of the result file
    """

    def execute(self):
        # If task is written in NCL:

            # Format the arguments for the NCL script.
            Input1 = "input1={0}".format(self.input1)
            Input2 = "input2={0}".format(self.input2)
            Filename = "filename=\"{0}\"".format(self.filename)
            # The workflow and task ids are used to create unique workflow folders and task files.
            wid = "wid=\"{0}\"".format(self.workflowID)
            tid = "tid=\"{0}\"".format(self.uid)
        
            # List of arguments to pass to NCL script
            # -Q argument removes output text, except errors, from the NCL scripts
            args = ['ncl','-Q', filename, Input1, Input2, wid, tid, '../plugin/workflow/python/customTasks/ncl/analysis-script.ncl']
            # Check for empty arguments, could be an argument is optional.
            args = filter(None,args)

            # Open a subprocess to run the analysis script with the given arguments.
            try:
                status = subprocess.call(args)
            # Catch errors
            except:
                sysError = True
                error = "System Error: Please contact the site administrator"
            if not sysError:
                # Common NCL errors
                if status:
                    if status == 2:
                        error = "NCL Error - Missing input parameter"
                    elif status == 3:
                        error = "NCL Error - Lat/Lon values out of range"
                    elif status == 4:
                        error = "NCL Error - Date value out of range"
                    elif status == 5:
                        error = "NCL Error - Invalid parameter value"
                    elif status == 6:
                        error = "NCL Error - Conversion error"
                    else:
                        error = "NCL Error - Error with NCL script"
                    nclError = True

            # Check that the output NetCDF file was created and return the filename as the task output.
            result = "data/{0}/{1}_subset.nc".format(self.workflowID, self.uid)
            if not sysError or not nclError:
                if not os.path.isfile(result):
                    error = "NCL Error - Error with NCL script"
                    nclError = True
            # If there is an error, return that instead of the output filename.
            if nclError or sysError:
                self.subset = error
            else:
                self.subset = result

        

        # If the task is written in R:

            # Import the R script to access its function.
            scriptname = "../plugin/workflow/python/customTasks/r/analysis-script.R"
            ro.r['source'](scriptname)

            # Check if workflow directory exists, if not create one
            wid = self.workflowID
            tid = self.id
            #Folder to store workflow files created by the task.
            workflowDirName = "python/data/" + str(wid) + "/"
            if not os.path.isdir(workflowDirName): os.system("mkdir " + workflowDirName)

            # Get path to the netcdf file
            infile = self.filename

            # Uniquely name output file by task id
            outfile = workflowDirName + str(tid) + "_task.nc"
            os.system("touch " + outfile)

            #Set variables for the R script
            Input1 = self.input1
            Input2 = self.input2

            # Call the function that does the calculation
            value = ro.r['analysisFunction'](infile, outfile, Input1, Input2)
            # Return the filename as the task output.
            self.result = "data/{0}/{1}_task.nc".format(wid,tid)