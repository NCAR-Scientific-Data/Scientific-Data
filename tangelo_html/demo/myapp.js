function subset() {
	var swLat = $("#swLat").val();
	var swLon = $("#swLon").val();
	var neLat = $("#neLat").val();
	var neLon = $("#neLon").val();
	var start = $("#start").val();
	var end = $("#end").val();
    $.getJSON("runSubset?swlat=" + encodeURIComponent(swLat) + "&swlon=" + encodeURIComponent(swLon) + "&nelat=" + encodeURIComponent(neLat) + "&nelon=" + encodeURIComponent(neLon) + "&startyear=" + encodeURIComponent(start) + "&endyear=" + encodeURIComponent(end), function (data) {
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
	var calc = $("#calc option:selected").val();
	var interval = $("#interval option:selected").val();
	var out = $("#outtime option:selected").val();
	alert("Calc: " + calc);
	$.getJSON("runAggregate?filename=" + encodeURIComponent(localStorage.getItem("subset")) + "&interval=" + encodeURIComponent(interval) + "&method=" + encodeURIComponent(calc) + "&outtime=" + encodeURIComponent(outtime), function (data) {
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
	$.getJSON("runPlot?filename=" + encodeURIComponent(localStorage.getItem("calculations")), function (data) {
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
