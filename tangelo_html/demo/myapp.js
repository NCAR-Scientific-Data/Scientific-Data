function runScript() {
        $.getJSON("runNCL", function (data) {
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
