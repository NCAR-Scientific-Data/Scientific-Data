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
    var url = "python/grabNetcdf?" + sim + v + swlat + swlon + nelat + nelon + start + end + rcm + gcm;
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
	var out = "&outtime=" + encodeURIComponent($("#outtime option:selected").val());
	var url = "python/runAggregate?filename=" + encodeURIComponent(localStorage.getItem("subset")) + interval + calc + out;
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
	var url = "python/runPlot?filename=" + encodeURIComponent(localStorage.result);
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

$("#sim").change(function() {
	var v = $("#sim option:selected").val();
	var start;
	var end;
	if(v === "ncep") {
		start = 1979;
		end = 2004;
	}
	else if (v === "-current") {
		start = 1970;
		end = 2000;
	}
	else {
		start = 2040;
		end = 2070;
	}

	$("syear").empty();
	$("eyear").empty();

	for(var i = start; i <= end; i++)
	{
		$("syear").append($('<option></option>').val(i).html(i.toString()));
		$("eyear").append($('<option></option>').val(i).html(i.toString()));
	}
});
