function threshold(filename, lower, upper) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "lower" : lower,
        "upper" : upper
    };

    console.log(inputs)

    addTask("taskPercentile", inputs, "result");
}

function callThreshold() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        lower = $("#lower").val,
        upper = $("#upper").val,

    var repopulateVals = {
        "html" : "stepHTML/threshold.html",
        "values" : {
            "#lower" : lower,
            "#upper" : upper
        }
    };

    percentile(filename, lower, upper);
}
