/*global $, addTask, updateTask*/

/*
	Title: Unit Conversion
*/

/*
	Function: unitConversion
	Creates the inputs and calls addTask.
*/
function unitConversion(filename, unit, repopulateVals ){
	"use strict";

	var inputs = {
		"filename" : filename,
		"unit" : unit
	};
	
	addTask("taskUnitConversion", inputs, repopulateVals, "result");
}

/*
	Function: callUnitConversion
	Parses the form and creates the repopulation values object.
*/
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

/*
	Function: updateUnitConversion
	Reparses the form and recreates the repopulation values, then calls updateTask.
*/
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

/*
	Function: generateNodeSelect
	Generates the dropdowns of nodes.
*/
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
