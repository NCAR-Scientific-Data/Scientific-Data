/*global $, addTask, updateTask*/

/*
    Title: Plot
*/

/*
    Functions: Plot Functions

    plot - Creates the inputs for the addTask call.
    callPlot - Parses the form data and creates the repopulation values.
    generateNodeSelect - Generates the dropdown of nodes.
*/

function plot(filename, timeindex, nativeP, repopulateVals) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "timeindex" : timeindex,
        "native" : nativeP
    };
    

    addTask("taskPlot", inputs, repopulateVals, "plot");
}

//Parse values from form
function callPlot() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        timeindex = $("#timeindex option:selected").val(),
        nativeP = $("input[name='native']:checked").val();

    var repopulateVals = {
        "html" : "stepHTML/plot.html",
        "values" : {
            "#timeindex" : timeindex,
            "#node" : selectedNode
        }
    };

    var nativePSelector = "input[name='" + nativeP + "']";

    repopulateVals.values[nativePSelector] = true;

    plot(filename, timeindex, nativeP, repopulateVals);
}

function updatePlot() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        timeindex = $("#timeindex option:selected").val(),
        nativeP = $("input[name='native']:checked").val();

    var repopulateVals = {
        "html" : "stepHTML/plot.html",
        "values" : {
            "#timeindex" : timeindex,
            "#node" : selectedNode
        }
    };

    var nativePSelector = "input[name='" + nativeP + "']";

    repopulateVals.values[nativePSelector] = true;

    var inputs = {
        "filename" : filename,
        "timeindex" : timeindex,
        "native" : nativeP
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