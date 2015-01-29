function runScript() {
		var swLat = $("#swLat").val();
		var swLon = $("#swLon").val();
		var neLat = $("#neLat").val();
		var neLon = $("#neLon").val();
		var start = $("#start").val();
		var end = $("#end").val();
        $.getJSON("runNCL?swlat=" + encodeURIComponent(swLat) + "&swlon=" + encodeURIComponent(swLon) + "&nelat=" + encodeURIComponent(neLat) + "&nelon=" + encodeURIComponent(neLon) + "&startyear=" + encodeURIComponent(start) + "&endyear=" + encodeURIComponent(end), function (data) {
		if(data.image)
		{
			localStorage.setItem("sourceimage", data.image);
			window.open("resultPage.html", "_self");
		}
		else
		{
			alert(data.alert);
		}
        });
}
