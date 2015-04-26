function percentile(filename, percentile) {
    "use strict";

    var inputs = {
        "filename" : filename,
        "percentile" : percentile,
    };

    console.log(inputs)

    addTask("taskPercentile", inputs, "result");
}

function callPercentile() {
    "use strict";

    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#node option:selected").val(),
        filename = ["Port", selectedNode, allNodes[selectedNode].output],
        percentile = $("#percentile").val,

    var repopulateVals = {
        "html" : "stepHTML/percentile.html",
        "values" : {
            "#percentile" : percentile,
        }
    };

    percentile(filename, percentile);
}
