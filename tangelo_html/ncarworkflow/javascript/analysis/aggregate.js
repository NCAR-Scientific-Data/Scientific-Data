/*global localStorage, $, addTask, updateTask*/

/*
    Title: Aggregate
*/

/*
    Functions: Aggregate Functions

    aggregate - Creates the inputs to pass to the add task parameters.
    callAggregate - Parses the form input, creates the repopulation values, and passes them to aggregate.
    generateNodeSelect - Populates the dropdown that takes in other nodes.
*/

function aggregate(filename, calc, interval, out, cyclic, repopulateVals) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "method" : calc,
        "interval" : interval,
        "outtime" : out,
        "cyclic" : cyclic
    };

    addTask("taskAggregate", inputs, repopulateVals, "result");
}

//Parse values from form
function callAggregate() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        calculation = $("#method option:selected").val(),
        interval = $("#interval option:selected").val(),
        out = $("#outtime option:selected").val(),
        cyclic = $("input[name='cyclic']:checked").val();

    var repopulateVals = {
        "html" : "stepHTML/aggregate.html",
        "values" : {
            "#calc" : calculation,
            "#node" : filename[1],
            "#interval" : interval,
            "#outtime" : out
        }
    };

    var cyclicSelector = "input[name='" + cyclic + "']";

    repopulateVals.values[cyclicSelector] = true;

    aggregate(filename, calculation, interval, out, cyclic, repopulateVals);
}

function updateAggregate() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        calculation = $("#method option:selected").val(),
        interval = $("#interval option:selected").val(),
        out = $("#outtime option:selected").val(),
        cyclic = $("input[name='cyclic']:checked").val();

    var repopulateVals = {
        "html" : "stepHTML/aggregate.html",
        "values" : {
            "#calc" : calculation,
            "#node" : filename[1],
            "#interval" : interval,
            "#outtime" : out
        }
    };

    var cyclicSelector = "input[name='" + cyclic + "']";

    repopulateVals.values[cyclicSelector] = true;

    var inputs = {
        "filename" : filename,
        "method" : calculation,
        "interval" : interval,
        "outtime" : out,
        "cyclic" : cyclic
    };

    updateTask(inputs, repopulateVals);
}

function generateNodeSelect(){
    "use strict";
    var nodeDropDown = $("#node");

    var nodes = JSON.parse(localStorage.nodes);

    for(var node in nodes){
        if (node != "workflowID"){
            var n = nodes[node];
            nodeDropDown.append($("<option></option>").val(node).html(n.name));
        }
    }
}