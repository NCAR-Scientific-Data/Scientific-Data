/*global $, addTask, updateTask*/

/*
    Title: Percentile
*/

/*
    Function: percentile
    Creates the inputs and calls addTask.
*/
function percentile(filename, percentile, repopulateVals) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "percentile" : percentile,
    };

    console.log(inputs)

    addTask("taskPercentile", inputs, repopulateVals, "result");
}

/*
    Function: callPercentile
    Parses the form and creates the repopulation values object.
*/
function callPercentile() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        percentile = $("#percentile").val(),

    var repopulateVals = {
        "html" : "stepHTML/percentile.html",
        "values" : {
            "#percentile" : percentile,
            "#node"       : selectedNode
        }
    };

    percentile(filename, percentile, repopulateVals);
}

/*
    Function: updatePercentile
    Reparses the form and recreates the repopulation values, then calls updateTask.
*/
function updatePercentile() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        percentile = $("#percentile").val(),

    var repopulateVals = {
        "html" : "stepHTML/percentile.html",
        "values" : {
            "#percentile" : percentile,
            "#node"       : selectedNode
        }
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

