function threshold(filename, field, lower, upper, repopulateVals) {
    "use strict";

    var inputs = {
        "filename" : filename,
	"field" : field,
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
        field = $("#field").val(),
	lower = $("#lower").val(),
        upper = $("#upper").val();

    var repopulateVals = {
        "html" : "stepHTML/threshold.html",
        "values" : {
            "#field" : field,
            "#lower" : lower,
            "#upper" : upper,
            "#node"  : selectedNode
        }
    };

    threshold(filename, field, lower, upper, repopulateVals);
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
