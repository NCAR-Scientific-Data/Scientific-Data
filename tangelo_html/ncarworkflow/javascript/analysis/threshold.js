/*global $, addTask, updateTask*/

/*
    Title: Threshold
*/

/*
    Functions: Threshold Functions

    threshold - Creates the inputs for the addTask call.
    callThreshold - Parses the form data and creates the repopulation values.
    updateThreshold - A combination of threshold and callThreshold, but instead of creating a new node it updates an existing one.
    generateNodeSelect - Generates the dropdown of nodes.
*/

function threshold(filename, lower, upper, repopulateVals) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "lower" : lower,
        "upper" : upper
    };

    addTask("taskThreshold", inputs, repopulateVals, "result");
}

function callThreshold() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
	lower = $("#lower").val(),
        upper = $("#upper").val();

    var repopulateVals = {
        "html" : "stepHTML/threshold.html",
        "values" : {
            "#lower" : lower,
            "#upper" : upper,
            "#node"  : selectedNode
        }
    };

    threshold(filename, lower, upper, repopulateVals);
}

function updateThreshold() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        lower = $("#lower").val(),
        upper = $("#upper").val();

    var repopulateVals = {
        "html" : "stepHTML/threshold.html",
        "values" : {
            "#lower" : lower,
            "#upper" : upper,
            "#node"  : selectedNode
        }
    };

    var inputs = {
        "filename" : filename,
        "lower" : lower,
        "upper" : upper
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
