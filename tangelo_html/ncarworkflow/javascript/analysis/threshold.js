function threshold(filename, lower, upper, repopulateVals) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "lower" : lower,
        "upper" : upper
    };

    console.log(inputs)

    addTask("taskThreshold", inputs, repopulateVals, "result");
}

function callThreshold() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        //filename = "tmin_subset_time_latlon.nc",
	lower = $("#lower").val,
        upper = $("#upper").val;

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
