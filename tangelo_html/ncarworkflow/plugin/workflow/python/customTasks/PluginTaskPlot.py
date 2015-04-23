import subprocess
import pyutilib.workflow
import os

#   Class: taskPlot
#   A task that plots.
class PluginTaskPlot(pyutilib.workflow.TaskPlugin):

    pyutilib.component.core.alias("taskPlot")
    alias = "taskPlot"

    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('filename')
        self.inputs.declare('timeindex')
        self.inputs.declare('native')
        self.outputs.declare('plot')
        
    def execute(self):
        sFilename = "filename=\"{0}\"".format(self.filename)
        if not self.timeindex:
                sTimeindex = "timeindex=0"
        else:
                sTimeindex = "timeindex={0}".format(self.timeindex)
        if self.native:
                plotScript = '../plugin/workflow/python/customTasks/ncl/plot_native.ncl'
        else:
                plotScript = '../plugin/workflow/python/customTasks/ncl/plot.ncl'
        wid = "wid=\"{0}\"".format(self.workflowID)
        tid = "tid=\"{0}\"".format(self.uid)

        args = ['ncl', '-n','-Q', wid, tid, sFilename, sTimeindex, plotScript]
        args = filter(None,args)
        sysError = False
        nclError = False

        try:
                status = subprocess.call(args)
        except:
                sysError = True
                error = "System error, please contact site administrator."
        if self.native:
                result = "/data/{0}/{1}_nativeplot.png".format(wid,tid)
        else:
                result = "/data/{0}/{1}_plot.png".format(self.workflowID,self.uid)
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