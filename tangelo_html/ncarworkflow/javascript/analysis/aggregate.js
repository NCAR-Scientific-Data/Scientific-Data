function callAggregate() {

	var calc = encodeURIComponent($("#calc option:selected").val());
	var interval = encodeURIComponent($("#interval option:selected").val());
	var out = encodeURIComponent($("#outtime option:selected").val());
	
	calculate(calc, interval, out);
}

function aggregate(calc, interval, out) {
	calc = "&method=" + calc;
	interval = "&interval=" + interval;
	out = "&outtime=" + out;
	url = "python/runCalculation?filename=" + encodeURIComponent(localStorage.getItem("subset")) + interval + calc + out;

	$("<p>Running Calculations. Please Wait.</p>").insertAfter($(".form-inline"));

	$.getJSON(url, function (data) {
		if(data.result)
		{
			localStorage.result = data.result;
			$("p").html("Calculations Succesful!");
		}
		else
		{
			localStorage.result = "";
			$("p").html("Calculations Failed.<br>" + data.error);
		}
    });
}