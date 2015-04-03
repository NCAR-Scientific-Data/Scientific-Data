function callPlot() {
	var filename = encodeURIComponent(localStorage.result);
	var timeindex = encodeURIComponent(0);
	var natively = encodeURIComponent("False");

	plot(filename, timeindex, natively);
}

function plot(filename, timeindex, natively)
{
	filename = "?filename=" + filename;
	timeindex = "&timeindex=" + timeindex;
	natively = "&native=" + natively;

	url = "python/runPlot" + filename + timeindex + natively;

	$("<p>Plotting. Please Wait.</p>").insertAfter($(".form-inline"));

	$.getJSON(url, function (data) {
		if(data.image)
		{
			document.getElementById("results").src = data.image;
			$("p").html("Calculations Succesful!");
			localStorage.clear();
		}
		else
		{
			$("p").html("Plotting Failed.<br>" + data.error);
		}
    });	
}