/*global localStorage, $*/

function aggregate(filename, calc, interval, out, cyclic, repopulateVals) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "calc" : calculation,
        "interval" : interval,
        "out" : out,
        "cyclic" : cyclic
    };

    addTask("taskAggregate", inputs, repopulateVals, "aggregate");
}

//Parse values from form
function callAggregate() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        calculation = $("#calc option:selected").val(),
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
    aggregate(filename, calc, interval, out, repopulateVals);
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