/*global localStorage, $, addTask, updateTask*/

/*
    Title: Delta
*/

/*
    Functions: Delta Functions

    delta - Creates the inputs to pass to the add task parameters.
    callDelta - Parses the form input, creates the repopulation values, and passes them to delta.
    updateDelta - Performs the same steps as callDelta and delta, but updates an existing node instead of creating a new one.
    generateNodeSelect - Populates the dropdown that takes in other nodes.
*/
function delta(filename1, filename2, repopulateVals) {
    "use strict";

    var inputs = {
        "filename1" : filename1,
	"filename2" : filename2
    };

    console.log(inputs)

    addTask("taskDelta", inputs, repopulateVals, "result");
}

function callDelta() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode1 = $("#node1 option:selected").val(),
        filename1 = ["Port", selectedNode1, allNodes[selectedNode1].output],
        selectedNode2 = $("#node2 option:selected").val(),
        filename2 = ["Port", selectedNode2, allNodes[selectedNode2].output];

    var repopulateVals = {
        "html" : "stepHTML/delta.html",
        "values" : {
            "#node1" : selectedNode1,
	    "#node2" : selectedNode2
        }
    };

    delta(filename1, filename2, repopulateVals);
}

function updateDelta() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode1 = $("#node1 option:selected").val(),
        filename1 = ["Port", selectedNode1, allNodes[selectedNode1].output],
        selectedNode2 = $("#node2 option:selected").val(),
        filename2 = ["Port", selectedNode2, allNodes[selectedNode2].output];

    var repopulateVals = {
        "html" : "stepHTML/delta.html",
        "values" : {
            "#node1"  : selectedNode1,
            "#node2"  : selectedNode2
        }
    };

    var inputs = {
        "filename1" : filename1,
	"filename2" : filename2
    };

    updateTask(inputs, repopulateVals);
}

function generateNodeSelect() {
    "use strict";
    var nodeDropDown1 = $("#node1");
    var nodeDropDown2 = $("#node2");

    var nodes = JSON.parse(localStorage.nodes);

    for(var node in nodes) {
        if (node !== "workflowID") {
            var n = nodes[node];
            nodeDropDown1.append($("<option></option>").val(node).html(n.name));
            nodeDropDown2.append($("<option></option>").val(node).html(n.name));
	    console.log(node);
        }
    }

    $("#node1:first-child").prop("selected", true);
    $("#node2:first-child").prop("selected", true);
}

