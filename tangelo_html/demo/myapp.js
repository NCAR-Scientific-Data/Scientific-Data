function runScript() {
        $.getJSON("runNCL?selat=" + encodeURIComponent(seLat) + "?selon=" + encodeURIComponent(seLon) + "?nwlat=" + encodeURIComponent("nwLat") + "?nwlon=" + encodeURIComponent("nwLon") + "?startyear=" + encodeURIComponent(start) + "?endyear=" + encodeURIComponent(end), function (data) {
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
