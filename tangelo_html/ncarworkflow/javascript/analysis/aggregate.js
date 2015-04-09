/*global localStorage, $*/

function aggregate(calc, interval, out) {
    "use strict";

    calc = "&method=" + calc;
    interval = "&interval=" + interval;
    out = "&outtime=" + out;
    var url = "python/runCalculation?filename=" + encodeURIComponent(localStorage.getItem("subset")) + interval + calc + out;

    $("<p>Running Calculations. Please Wait.</p>").insertAfter($(".form-inline"));

    $.getJSON(url, function (data) {
        if (data.result) {
            localStorage.result = data.result;
            $("p").html("Calculations Succesful!");
        } else {
            localStorage.result = "";
            $("p").html("Calculations Failed.<br>" + data.error);
        }
    });
}

function callAggregate() {
    "use strict";

    var calc = encodeURIComponent($("#calc option:selected").val()),
        interval = encodeURIComponent($("#interval option:selected").val()),
        out = encodeURIComponent($("#outtime option:selected").val());

    aggregate(calc, interval, out);
}