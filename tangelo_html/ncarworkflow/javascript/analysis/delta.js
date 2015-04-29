
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

