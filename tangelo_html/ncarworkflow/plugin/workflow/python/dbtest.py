from pymongo import MongoClient

def saveWorkflow(workflowID, data, repop):
	# open mongodb client and database
	client = MongoClient()
	db = client.database
	collection = db.workflows
	
	return collection.update_one({"_id": workflowID}, {'$set': {'data': data, 'repop': repop}}, upsert = True)

workflowID = 19203923845
json = {"x": [{'test': "yes", "y":"no"},{"Z":"meh", "A":"okay"}], "masks":{"id":"valore"}, "om_points":"value"}

saveWorkflow(workflowID, json, 24)
