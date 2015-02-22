//Creating/Using Steps----------------------------------------------------------
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
//------------------------------------------------------------------------------

//Manipulating NetCDFs----------------------------------------------------------
function subset() {
	var simulationType = "simulationType=" + $("#simulationType option:selected").val();
	var variable = "&variable=" + $("input[name='variable']:checked").val();
	var swlat = "&swlat=" + $("#swlat").val();
	var swlon = "&swlon=" + $("#swlon").val();
	var nelat = "&nelat=" + $("#nelat").val();
	var nelon = "&nelon=" + $("#nelon").val();
	var timestart = "&timeStart=" + $("#startYear option:selected").val() + "-" + $("#startMonth option:selected").val() + "-" + $("#startDay option:selected").val();
	var timeend = "&timeEnd=" + $("#endYear option:selected").val() + "-" + $("#endMonth option:selected").val() + "-" + $("#endDay option:selected").val();
    var rcm = "&rcm=" + $("input[name='rcm']:checked").val();
    var gcm = "&gcm=" + $("input[name='gcm']:checked").val();
    var url = "python/grabNetcdf?" + simulationType + variable + swlat + swlon + nelat + nelon + timestart + timeend + rcm + gcm;

    $("<p>Subsetting. Please Wait.</p>").insertAfter($("button"));

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
//------------------------------------------------------------------------------

//Subset Functions--------------------------------------------------------------
function changeDateRange(simulationType)
{
	var start;
	var end;
	if(simulationType === "ncep") {
		start = 1979;
		end = 2004;
	}
	else if (simulationType === "-current") {
		start = 1970;
		end = 2000;
	}
	else {
		start = 2040;
		end = 2070;
	}
	var startYearDropDown = $("#startYear");
	var endYearDropDown = $("#endYear");

	startYearDropDown.empty();
	endYearDropDown.empty();

	for(i = start; i <= end; i++)
	{
		startYearDropDown.append($('<option></option>').val(i).html(i.toString()));
		endYearDropDown.append($('<option></option>').val(i).html(i.toString()));
	}
}

function changeGCM(simulationType, rcm)
{
	var ccsm = $("#ccsm");
	var cgcm3 = $("#cgcm3");
	var gfdl = $("#gfdl");
	var hadcm3 = $("#hadcm3");

	$("input[name='gcm']").each(function() {
		$(this).attr("disabled", true);
	})

	if(simulationType === "ncep") {
		$("#none").attr('disabled', false);

		$("#none").prop('checked', true);
	}
	else {
		if(rcm === "crcm") {
			ccsm.attr('disabled',false);
			cgcm3.attr('disabled',false);

			ccsm.prop('checked', true);
		}
		else if(rcm === "ecp2") {
			gfdl.attr('disabled',false);

			gfdl.prop('checked', true);
		}
		else if(rcm === "hrm3") {
			gfdl.attr('disabled',false);
			hadcm3.attr('disabled',false);

			gfdl.prop('checked', true);
		}
		else if(rcm === "mm5i") {
			ccsm.attr('disabled',false);

			ccsm.prop('checked', true);

			if(simulationType === "-current") {
				hadcm3.attr('disabled',false);
			}
		}
		else if(rcm === "rcm3") {
			gfdl.attr('disabled',false);
			cgcm3.attr('disabled',false);

			gfdl.prop('checked', true);
		}
		else if(rcm === "wrfg") {
			ccsm.attr('disabled',false);
			cgcm3.attr('disabled',false);

			ccsm.prop('checked', true);
		}
	}
}

function changeBasedOnSim()
{
	var simulationType = $("#simulationType option:selected").val();
	var rcm = $("input[name='rcm']:checked").val();

	changeDateRange(simulationType);
	changeGCM(simulationType, rcm);
}

function changeBasedOnRCM()
{
	var simulationType = $("#simulationType option:selected").val();
	var rcm = $("input[name='rcm']:checked").val();
	
	changeGCM(simulationType, rcm);
}
//------------------------------------------------------------------------------

$(document).ready(newStep);