import subprocess
import pyutilib.workflow
import os

#   Class: PluginTaskPlot
#   A task that plots NetCDF data.
#
#   Attributes:
#
#       filename - The name of the NetCDF file to plot.
#       timeindex - The time index of which to plot.
#       native - Whether to plot using a standard projection or the native projection.
class PluginTaskPlot(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskPlot")
    alias = "taskPlot"
    #   Constructor: __init__
    #   Creates a Plot task
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #       *args - A list of arguments.
    #       **kwds - A list of keyword arguments.
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('filename')
        self.inputs.declare('timeindex')
        self.inputs.declare('native')
        self.outputs.declare('plot')
        
    #   Function: execute
    #   Calls the NCL script to plot the NetCDF file.
    #
    #   Parameters:
    #
    #       self - A reference to the object.
    #
    #   Returns:
    #
    #       The path of the resulting png plot image.
    def execute(self):
        sFilename = "filename=\"{0}\"".format(self.filename)
        if not self.timeindex:
                sTimeindex = "timeindex=0"
        else:
                sTimeindex = "timeindex={0}".format(self.timeindex)
        if self.native == "True":
                plotScript = '../plugin/workflow/python/customTasks/ncl/plot_native.ncl'
        else:
                plotScript = '../plugin/workflow/python/customTasks/ncl/plot.ncl'
        wid = "wid=\"{0}\"".format(self.workflowID)
        tid = "tid=\"{0}\"".format(self.uid)

        args = ['ncl', '-Q', wid, tid, sFilename, sTimeindex, plotScript]
        args = filter(None,args)
        sysError = False
        nclError = False

        try:
                status = subprocess.call(args)
        except:
                sysError = True
                error = "System error, please contact site administrator."
        if self.native == "True":
                result = "data/{0}/{1}_nativeplot.png".format(self.workflowID,self.uid)
        else:
                result = "data/{0}/{1}_plot.png".format(self.workflowID,self.uid)
        if not sysError:
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
        if not sysError or not nclError:
            if not os.path.isfile(result):
                error = "NCL Error - Please check input parameters."
                nclError = True
        if nclError or sysError:
                self.plot = error
        else:
                self.plot = result
