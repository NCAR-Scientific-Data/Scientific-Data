import pyutilib.workflow
import uuid
import sys
sys.path.insert(1,'/home/project/Scientific-Data/tangelo_html/ncarworkflow/plugin/workflow/python/customTasks/')
from taskThreshold import taskThreshold

def createWorkflow():
	A = taskThreshold()
	w = pyutilib.workflow.Workflow()
	A.inputs.filename = "tmin_subset_time_latlon.nc"
	A.inputs.lower = "25"
	A.inputs.upper = "27"
	w.add(A)
	#w.setWorkflowID(423)
	test = w()
createWorkflow()
