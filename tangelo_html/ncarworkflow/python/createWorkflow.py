import pyutilib.workflow
import uuid
import json

# Serialize workflow into json file with UID as filename
def serialize(workflow):
	with open('data/'+str(workflow.workflowID)+'.json', 'w') as outfile:
		json.dump(workflow.__dict__(), outfile)

def run():
	uid = uuid.uuid4()
	w = pyutilib.workflow.Workflow()
	w.setWorkflowID(uid)
	serialize(w)
	return { "uid" : str(uid) }