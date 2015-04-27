/*global $, addTask, updateTask*/

function unitConversion(filename, unit, repopulateVals ){
	"use strict";

	var inputs = {
		"filename" : filename,
		"unit" : unit
	};
	
	addTask("taskUnitConversion", inputs, repopulateVals, "result");
}

//Parse values from form
function callUnitConversion(){
	"use strict";

	var allNodes = JSON.parse(localStorage.nodes),
	selectedNode = $("#node option:selected").val(),
	filename = ["Port", selectedNode, allNodes[selectedNode].output],
	unit = $("#unit option:selected").val();

	var repopulateVals = {
		"html" : "stepHTML/unitConversion.html",
		"values" : {
			"#unit" : unit,
			"#node" : filename[1]
		}
	};

	unitConversion(filename, unit, repopulateVals);
}

function updateUnitConversion() {
	"use strict";

	var allNodes = JSON.parse(localStorage.nodes),
	selectedNode = $("#node option:selected").val(),
	filename = ["Port", selectedNode, allNodes[selectedNode].output],
	unit = $("#unit option:selected").val();

	var repopulateVals = {
		"html" : "stepHTML/unitConversion.html",
		"values" : {
			"#unit" : unit,
			"#node" : filename[1]
		}
	};

	var inputs = {
		"filename" : filename,
		"unit" : unit
	};

	updateTask(inputs, repopulateVals);
}

function generateNodeSelect() {
    "use strict";
    var nodeDropDown = $("#node");

    var nodes = JSON.parse(localStorage.nodes);

    for(var node in nodes) {
        if (node !== "workflowID") {
            var n = nodes[node];
            nodeDropDown.append($("<option></option>").val(node).html(n.name));
        }
    }

    $("#node:first-child").prop("selected", true);
}
