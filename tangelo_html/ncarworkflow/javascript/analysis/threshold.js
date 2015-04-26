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
            "#upper" : upper
        }
    };

    threshold(filename, lower, upper, repopulateVals);
}
