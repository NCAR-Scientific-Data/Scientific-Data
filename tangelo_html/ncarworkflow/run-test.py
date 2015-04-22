import pyutilib.workflow
import uuid
import sys
sys.path.insert(1,'/home/project/Scientific-Data/tangelo_html/ncarworkflow/plugin/workflow/python/customTasks/')
from taskThreshold import taskThreshold
from taskDelta import taskDelta
from taskPercentile import taskPercentile
def createWorkflow():
	w = pyutilib.workflow.Workflow()

	# Test threshold
	A = taskThreshold()
	A.inputs.filename = "tmin_subset_time_latlon.nc"
	A.inputs.lower = "25"
	A.inputs.upper = "27"
	
	# Test delta
	A = taskDelta()
	A.inputs.filename1 = "tmin_subset_time_latlon.nc"
	A.inputs.filename2 = "tmin_subset_time_latlon.nc"	

	# Test percentile
	A = taskPercentile()
	A.inputs.filename = "tmin_subset_time_latlon.nc"
	A.inputs.percentile = 75

	w.add(A)
	#w.setWorkflowID(423)
	test = w()
createWorkflow()
