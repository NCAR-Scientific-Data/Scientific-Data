function newStep() {
	$("main").load("chooseStep.html");
}

function createPage(page) {
	$("main").load(page);
	insertStep(page.substring(0,page.length-5), null);
}

function insertStep(stepName, stepValues) {
	var newstep = "<a onclick=createPage('" + stepName + ".html')>" + stepName + "</a>";
	$(newstep).insertBefore($("aside a:last"));
}

function subset() {
	var simulationType = "simulationType=" + $("#simulationType option:selected").val();
	var variable = "&variable=" + $("input[name='variable']:checked").val();
	var swlat = "&swlat=" + $("#swlat").val();
	var swlon = "&swlon=" + $("#swlon").val();
	var nelat = "&nelat=" + $("#nelat").val();
	var nelon = "&nelon=" + $("#nelon").val();
	var timestart = "&timeStart=" + $("#startYear option:selected").val() + "-" + $("#startMonth option:selected").val() + "-" + $("#sDay option:selected").val();
	var timeend = "&timeEnd=" + $("#eyear option:selected").val() + "-" + $("#emonth option:selected").val() + "-" + $("#eday option:selected").val();
    var rcm = "&rcm=" + $("input[name='rcm']:checked").val();
    var gcm = "&gcm=" + $("input[name='gcm']:checked").val();
    var url = "python/grabNetcdf?" + sim + v + swlat + swlon + nelat + nelon + start + end + rcm + gcm;

    $("<p>Subsetting. Please Wait.").insertAfter($("form"));

    $.getJSON(url, function (data) {
		if(data.subset)
		{
			$("p").innerHTML("Subset Succesful!");
			localStorage.subset = data.subset;

		}
		else
		{
			$("p").innerHTML("Subset Failed.<br>" + data.alert)
			localStorage.subset = "";
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
	var filename = "?filename=" + encodeURIComponent(localStorage.result);
	var timeindex = "&timeindex=" + encodeURIComponent(0);
	var natively = "&native=" + encodeURIComponent("False");
	var url = "python/runPlot" + filename + timeindex + natively;
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

function changeDateRange()
{
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

	$("#syear").empty();
	$("#eyear").empty();

	for(i = start; i <= end; i++)
	{
		$("#syear").append($('<option></option>').val(i).html(i.toString()));
		$("#eyear").append($('<option></option>').val(i).html(i.toString()));
	}
}

function changeGCM()
{
	var sim = $("#sim option:selected").val();
	var rcm = $("input[name='rcm']:checked").val();

	if(sim === "ncep") {
		$("input[name='gcm']").each(function(){
			if($(this).val() !== "") {
				$(this).attr('disabled',true);
			}
			else {
				$(this).attr('disabled',false);
				$(this).prop('checked',true);
			}
		});
	}
	else {
		if(rcm === "crcm") {
			$("input[name='gcm']").each(function(){
				$(this).attr('disabled',true);
			});
			$('#CCSM').attr('disabled',false);
			$('#CCSM').prop('checked', true);
			$('#CGCM3').attr('disabled',false);
		}
		else if(rcm === "ecp2") {
			$("input[name='gcm']").each(function(){
				$(this).attr('disabled',true);
			});
			$('#GFDL').attr('disabled',false);
			$('#GFDL').prop('checked', true);
		}
		else if(rcm === "hrm3") {
			$("input[name='gcm']").each(function(){
				$(this).attr('disabled',true);
			});
			$('#GFDL').attr('disabled',false);
			$('#HADCM3').attr('disabled',false);
			$('#GFDL').prop('checked', true);
		}
		else if(rcm === "mm5i") {
			$("input[name='gcm']").each(function(){
				$(this).attr('disabled',true);
			});
			$('#CCSM').attr('disabled',false);
			$('#CCSM').prop('checked', true);
			if(sim === "-current") {
				$('#HADCM3').attr('disabled',false);
			}
		}
		if(rcm === "rcm3") {
			$("input[name='gcm']").each(function(){
				$(this).attr('disabled',true);
			});
			$('#GFDL').attr('disabled',false);
			$('#CGCM3').attr('disabled',false);
			$('#GFDL').prop('checked', true);
		}
		if(rcm === "wrfg") {
			$("input[name='gcm']").each(function(){
				$(this).attr('disabled',true);
			});
			$('#CCSM').attr('disabled',false);
			$('#CGCM3').attr('disabled',false);
			$('#CCSM').prop('checked', true);
		}
	}
}

function changeBasedOnSim()
{
	changeDateRange();
	changeGCM();
}

function changeBasedOnRCM()
{
	changeGCM();
}

$(document).ready(newStep);