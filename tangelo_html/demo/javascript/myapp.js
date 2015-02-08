function subset() {
	var sim = "simulation_type=" + $("#sim option:selected").val();
	var v = "&variable=" + $("input[name='var']:checked").val();
	var swlat = "&swLat=" + $("#swlat").val();
	var swlon = "&swLon=" + $("#swlon").val();
	var nelat = "&neLat=" + $("#nelat").val();
	var nelon = "&neLon=" + $("#nelon").val();
	var start = "&timestart=" + $("#syear option:selected").val() + "-" + $("#smonth option:selected").val() + "-" + $("#sday option:selected").val();
	var end = "&timeend=" + $("#eyear option:selected").val() + "-" + $("#emonth option:selected").val() + "-" + $("#eday option:selected").val();
    var rcm = "&rcm=" + $("input[name='rcm']:checked").val();
    var gcm = "&gcm=" + $("input[name='gcm']:checked").val();
    url = "python/grabNetcdf?" + sim + v + swlat + swlon + nelat + nelon + start + end + rcm + gcm
    $.getJSON(url, function (data) {
		if(data.subset)
		{
			localStorage.subset = data.subset;
			window.open("calculate.html", "_self");
		}
		else
		{
			localStorage.subset = "";
			alert(data.alert);
		}
    });
}

function calculate() {

	document.getElementById("submitMessage").innerHTML = "<p>Your results are being calculated.</p>"

	var calc = "&method=" + encodeURIComponent($("#calc option:selected").val());
	var interval = "&interval=" + encodeURIComponent($("#interval option:selected").val());
	var out = "&outtime" + encodeURIComponent($("#outtime option:selected").val());
	var url = "runAggregate?filename=" + encodeURIComponent(localStorage.getItem("subset")) + interval + calc + out;
	$.getJSON(url, function (data) {
		if(data.result)
		{
			localStorage.result = data.result;
			window.open("resultPage.html", "_self");
		}
		else
		{
			localStorage.result = "";
			alert(data.alert);
		}
        });
}

function plot()
{
	var url = "runPlot?filename=" + encodeURIComponent(localStorage.result);
	$.getJSON(url, function (data) {
		if(data.image)
		{
			document.getElementById("results").src = data.image;
			document.getElementById("waitMessage").innerHTML = "";
			localStorage.clear();
		}
		else
		{
			document.getElementById("waitMessage").innerHTML = data.alert;
		}
    });	
}