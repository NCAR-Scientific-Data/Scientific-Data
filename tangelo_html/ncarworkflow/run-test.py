import pyutilib.workflow
import uuid
import sys
sys.path.insert(1,'/home/project/Scientific-Data/tangelo_html/ncarworkflow/plugin/workflow/python/customTasks')
from PluginTaskThreshold import PluginTaskThreshold
from PluginTaskSubset import PluginTaskSubset
from PluginTaskDelta import PluginTaskDelta
#from taskPercentile import taskPercentile
#from
def createWorkflow():
	w = pyutilib.workflow.Workflow()

	# Test threshold
	#A = PluginTaskThreshold()
	#w = pyutilib.workflow.Workflow()
	#A.inputs.filename = "tmin_subset_time_latlon.nc"
	#A.inputs.lower = "25"
	#A.inputs.upper = "27"
	
	# Test delta
	A = PluginTaskDelta()
	A.inputs.filename1 = "tmin_subset_time_latlon.nc"
	A.inputs.filename2 = "tmin_subset_time_latlon.nc"	

	# Test percentile
	#A = taskPercentile()
	#A.inputs.filename = "tmin_subset_time_latlon.nc"
	#A.inputs.percentile = 75

	#setUID(2015422)
	#w.setWorkflowID(2015422)
	#A.setWorkflowID(2015)
	#w = pyutilib.workflow.Workflow()
	w.add(A)
	#print A
	#print w
	#w.add(A)
	#w.setWorkflowID(2015)
	#w.setWorkflowID(2015422)
	#w.setWorkflowID(423)
	test = w()
createWorkflow()
