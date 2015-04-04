import pyutilib.workflow
import uuid
import sys
sys.path.insert(1,'C:/Users/Hannah/Documents/Scientific-Data/tangelo_html/ncarworkflow/python')
from TaskSubset import taskSubset
from TaskAggregate import taskAggregate


def createWorkflow():
	A = taskSubset()
	B = taskAggregate()
	w = pyutilib.workflow.Workflow()
	A.inputs.url = "tmin.CRCM.ncep.dayavg.native.nc"
	A.inputs.variable = "tmin"
	A.inputs.swlat = 35
	A.inputs.swlon = 255
	A.inputs.nelat = 45
	A.inputs.nelon = 265
	A.inputs.startdate = "1990-01-01"
	A.inputs.enddate = "2000-01-01"
	B.inputs.filename = A.outputs.subset
	B.inputs.variable = "tmin"
	B.inputs.interval = "month"
	B.inputs.method = "mean"
	B.inputs.outtime = "start"
	B.inputs.cyclic = False
	A.setWorkflowID(2222)
	B.setWorkflowID(2222)
	w.add(A)
	w.add(B)
	w.setWorkflowID(2222)
	test = w()
createWorkflow()