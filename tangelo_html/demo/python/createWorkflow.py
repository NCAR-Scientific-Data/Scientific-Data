import pyutilib.workflow
import uuid

def run():
	uid = uuid.uuid4()
	w = pyutilib.workflow.Workflow()
	w.setWorkflowID(uid)
	return {"uid":uid}