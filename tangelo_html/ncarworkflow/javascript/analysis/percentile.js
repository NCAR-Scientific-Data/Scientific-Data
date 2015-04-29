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

