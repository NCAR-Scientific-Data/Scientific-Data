/*global $, confirm, alert*/

/*
	Function: loadWorkflow
    Load a workflow given a workflow ID.

   	Once a workflow is loaded, the user has the option to download the results,
   	and then is further asked if they want to edit the workflow. If a user chooses
   	to edit the  workflow, then the page redirects to the workflow builder.

    See Also:

        <saveWorkflow>
*/
function loadWorkflow() {
	"use strict";

	var workflowID = $("#serialNum").val(),
		url = "python/updateWorkflow",
		stuffToPass = {
			"function" : "loadWorkflow",
			"workflowID" : workflowID,
			"args" : JSON.stringify([])
		};

	$.getJSON(url, stuffToPass, function (results) {
		if (results.result) {
			var re = new RegExp("^.+[.](png|nc)$");
			if (re.test(results.result)) {
			    var download = confirm("Workflow Resulted In:\n" + results.result + ".\n Would you like to download?");

			    if (download) {
			        window.open("python/" + results.result);
			    }

			} else {
			    alert("Results of Workflow:\n" + results.result);
			}

			var edit = confirm("Would you like to edit this workflow?");

			if (edit) {
				var repop = JSON.parse(results.repop);
				localStorage.uid = repop.workflowID;
				localStorage.nodes = results.repop;
				localStorage.workflow = JSON.stringify(results.workflow);
				window.location.replace("workflow-builder.html");
			}
		}
	});
}
