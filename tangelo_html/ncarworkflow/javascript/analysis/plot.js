/*global localStorage, $, document*/
function plot(filename, timeindex, natively) {
    "use strict";
    filename = "?filename=" + filename;
    timeindex = "&timeindex=" + timeindex;
    natively = "&native=" + natively;

    var url = "python/runPlot" + filename + timeindex + natively;

    $("<p>Plotting. Please Wait.</p>").insertAfter($(".form-inline"));

    $.getJSON(url, function (data) {
        if (data.image) {
            document.getElementById("results").src = data.image;
            $("p").html("Calculations Succesful!");
            localStorage.clear();
        } else {
            $("p").html("Plotting Failed.<br>" + data.error);
        }
    });
}

function callPlot() {
    "use strict";
    var filename = encodeURIComponent(localStorage.result),
        timeindex = encodeURIComponent(0),
        natively = encodeURIComponent("False");

    plot(filename, timeindex, natively);
}

