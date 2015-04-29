function climatology(filename, startmonth, endmonth, repopulateVals) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "startmonth" : startmonth,
        "endmonth" : endmonth
    };

    console.log(inputs)

    addTask("taskPercentile", inputs, repopulateVals, "result");
}

function callClimatology() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        startmonth = $("#startmonth").val(),
        endmonth = $("#endmonth").val();

    var repopulateVals = {
        "html" : "stepHTML/climatology.html",
        "values" : {
            "#startmonth" : startmonth,
            "#endmonth"   : endmonth,
            "#node"       : selectedNode
        }
    };

    climatology(filename, startmonth, endmonth, repopulateVals);
}

function updateClimatology() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        startmonth = $("#startmonth").val(),
        endmonth = $("#endmonth").val();

    var repopulateVals = {
        "html" : "stepHTML/climatology.html",
        "values" : {
            "#startmonth" : startmonth,
            "#endmonth" : endmonth,
            "#node"  : selectedNode
        }
    };

    var inputs = {
        "filename" : filename,
        "startmonth" : startmonth,
        "endmonth" : endmonth
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

