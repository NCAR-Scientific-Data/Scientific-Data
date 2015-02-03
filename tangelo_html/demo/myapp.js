function subset() {
	var swLat = "swlat=" + encodeURIComponent($("#swLat").val());
	var swLon = "&swlon=" + encodeURIComponent($("#swLon").val());
	var neLat = "&nelat=" + encodeURIComponent($("#neLat").val());
	var neLon = "&nelon=" + encodeURIComponent($("#neLon").val());
	var start = "&startyear=" + encodeURIComponent($("#start").val());
	var end = "&endyear=" + encodeURIComponent($("#end").val());
	var url = "runSubset?" + swLat + swLon + neLat + neLon + start + end;
    $.getJSON(url, function (data) {
		if(data.subset)
		{
			localStorage.setItem("subset", data.subset);
			window.open("calculate.html", "_self");
		}
		else
		{
			alert(data.alert);
		}
    });
}

function calculate() {
	var calc = "&method=" + encodeURIComponent($("#calc option:selected").val());
	var interval = "&interval=" + encodeURIComponent($("#interval option:selected").val());
	var out = "&outtime" + encodeURIComponent($("#outtime option:selected").val());
	var url = "runAggregate?filename=" + encodeURIComponent(localStorage.getItem("subset")) + interval + calc + out;
	$.getJSON(url, function (data) {
		if(data.result)
		{
			localStorage.setItem("calculations", data.result);
			window.open("resultPage.html", "_self");
		}
		else
		{
			alert(data.alert);
		}
        });
}

function plot()
{
	var url = "runPlot?filename=" + encodeURIComponent(localStorage.getItem("calculations"));
	$.getJSON(url, function (data) {
		if(data.image)
		{
			document.getElementById("results").src = data.image;
			document.getElementById("waitMessage").innerHTML = "";
			localStorage.removeItem("calculations");
			localStorage.removeItem("subset");

		}
		else
		{
			alert(data.alert);
		}
    });	
}
