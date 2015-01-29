function runScript() {
        $.getJSON("runNCL?swlat=" + encodeURIComponent(swLat) + "&swlon=" + encodeURIComponent(swLon) + "&nelat=" + encodeURIComponent("neLat") + "&nelon=" + encodeURIComponent("neLon") + "&startyear=" + encodeURIComponent(start) + "&endyear=" + encodeURIComponent(end), function (data) {
		if(data.image)
		{
			localStorage.setItem("sourceimage?", data.image);
			alert("Made it!");
			//window.open("resultPage.html", "_self");
		}
		else
		{
			alert(data.alert);
		}
        });
}
