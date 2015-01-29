function runScript() {
        $.getJSON("runNCL?swlat=" + encodeURIComponent(swLat) + "&swlon=" + encodeURIComponent(swLon) + "&nelat=" + encodeURIComponent("neLat") + "&nelon=" + encodeURIComponent("neLon") + "&startyear=" + encodeURIComponent(start) + "&endyear=" + encodeURIComponent(end), function (data) {
		if(data.image)
		{
			localStorage.setItem("sourceimage?", data.image);
			window.open("resultPage.html", "_self");
		}
		else
		{
			alert(data.alert);
		}
        });
}
