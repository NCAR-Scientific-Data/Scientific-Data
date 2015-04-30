/*global localStorage, $, addTask, updateTask*/

/*
    Title: Percentile
*/

/*
    Functions: Percentile Functions

    percentile - Creates the inputs to pass to the add task parameters.
    callPercentile - Parses the form input, creates the repopulation values, and passes them to percentile.
    updatePercentile - Performs the same steps as callPercentile and percentile, but updates an existing node instead of creating a new one.
    generateNodeSelect - Populates the dropdown that takes in other nodes.
*/
function percentile(filename, percentage, repopulateVals) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "percentage" : percentage
    };

    console.log(inputs)

    addTask("taskPercentile", inputs, repopulateVals, "result");
}

function callPercentile() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        percentage = $("#percentage").val();

    var repopulateVals = {
        "html" : "stepHTML/percentile.html",
        "values" : {
            "#percentage" : percentage,
            "#node"       : selectedNode
        }
    };

    percentile(filename, percentage, repopulateVals);
}

function updatePercentile() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        percentage = $("#percentage").val();

    var repopulateVals = {
        "html" : "stepHTML/percentile.html",
        "values" : {
            "#percentage" : percentage,
            "#node"  : selectedNode
        }
    };

    var inputs = {
        "filename" : filename,
        "percentage" : percentage
    };

    updateTask(inputs, repopulateVals);
}

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

