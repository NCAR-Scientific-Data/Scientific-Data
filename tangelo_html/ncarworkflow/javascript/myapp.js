//Creating/Using Steps----------------------------------------------------------
function newStep() {
	$("aside a").removeClass("active");
	$("aside a:last").addClass("active");
	$("main").load("chooseStep.html");
}

function createStep(step, isNew, id) {
	$("main").load(step + ".html");
	if(isNew)
	{
		insertStep(step, null);
	}
	else
	{
		$("aside a").removeClass("active");
		$("#"+id).addClass("active");
	}	
}

function deleteStep() {
	var startId = Number($(".active").attr("id"));
	$("aside a.active").nextAll().each(function (index) {
		if($(this).attr('id') != 0)
		{
			$(this).attr('id', startId);
			startId+= 1;
		}
	});
	$(".active").remove();
	newStep();
}

function insertStep(stepName, stepValues) {
	var id= $("aside a").length;
	var idfull = "id=\"" + id +"\"";
	var onclick = "onclick=\"createStep('" + stepName + "', false, this.id)\"";
	
	var newstep = "<a " + idfull + onclick + ">" + stepName + "</a>";
	$(newstep).insertBefore($("aside a:last"));
	$("aside a").removeClass("active");
	$("#" + id).addClass("active");
}
//------------------------------------------------------------------------------

//Manipulating NetCDFs----------------------------------------------------------
function callSubset() {
	var simulationType = $("#simulationType option:selected").val();
	var variable = $("input[name='variable']:checked").val();
	var swlat = $("#swlat").val();
	var swlon = $("#swlon").val();
	var nelat = $("#nelat").val();
	var nelon = $("#nelon").val();
	var timestart = $("#startYear option:selected").val() + "-" + $("#startMonth option:selected").val() + "-" + $("#startDay option:selected").val();
	var timeend = $("#endYear option:selected").val() + "-" + $("#endMonth option:selected").val() + "-" + $("#endDay option:selected").val();
    var rcm = $("input[name='rcm']:checked").val();
    var gcm = $("input[name='gcm']:checked").val();

    subset(simulationType, variable, swlat, swlon, nelat, nelon, timestart, timeend, rcm, gcm);
}

function subset(simulationType, variable, swlat, swlon, nelat, nelon, timestart, timeend, rcm, gcm) {
	simulationType = "simulationType=" + simulationType;
	variable = "&variable=" + variable;
	swlat = "&swlat=" + swlat;
	swlon = "&swlon=" + swlon;
	nelat = "&nelat=" + nelat;
	nelon = "&nelon=" + nelon;
	timestart = "&timeStart=" + timestart;
	timeend = "&timeEnd=" + timeend;
    rcm = "&rcm=" + rcm;
    gcm = "&gcm=" + gcm;
    url = "python/grabNetcdf?" + simulationType + variable + swlat + swlon + nelat + nelon + timestart + timeend + rcm + gcm;

    $("<p>Subsetting. Please Wait.</p>").insertAfter($(".form-inline"));

    $.getJSON(url, function (data) {
		if(data.subset)
		{
			$("p").html("Subset Succesful!");
			localStorage.subset = data.subset;

		}
		else
		{
			$("p").html("Subset Failed.<br>" + data.error);
			localStorage.subset = "";
		}
    });
}

function callCalculate() {

	var calc = encodeURIComponent($("#calc option:selected").val());
	var interval = encodeURIComponent($("#interval option:selected").val());
	var out = encodeURIComponent($("#outtime option:selected").val());
	
	calculate(calc, interval, out);
}

function calculate(calc, interval, out) {
	calc = "&method=" + calc;
	interval = "&interval=" + interval;
	out = "&outtime=" + out;
	url = "python/runCalculation?filename=" + encodeURIComponent(localStorage.getItem("subset")) + interval + calc + out;

	$("<p>Running Calculations. Please Wait.</p>").insertAfter($(".form-inline"));

	$.getJSON(url, function (data) {
		if(data.result)
		{
			localStorage.result = data.result;
			$("p").html("Calculations Succesful!");
		}
		else
		{
			localStorage.result = "";
			$("p").html("Calculations Failed.<br>" + data.error);
		}
    });
}

function callPlot() {
	var filename = encodeURIComponent(localStorage.result);
	var timeindex = encodeURIComponent(0);
	var natively = encodeURIComponent("False");

	plot(filename, timeindex, natively);
}

function plot(filename, timeindex, natively)
{
	filename = "?filename=" + filename;
	timeindex = "&timeindex=" + timeindex;
	natively = "&native=" + natively;

	url = "python/runPlot" + filename + timeindex + natively;

	$("<p>Plotting. Please Wait.</p>").insertAfter($(".form-inline"));

	$.getJSON(url, function (data) {
		if(data.image)
		{
			document.getElementById("results").src = data.image;
			$("p").html("Calculations Succesful!");
			localStorage.clear();
		}
		else
		{
			$("p").html("Plotting Failed.<br>" + data.error);
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
	
	$("#endYear option:last-child").prop("selected", true);
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

			cgcm3.prop('checked', true);
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

			if(simulationType === "-current") {
				hadcm3.attr('disabled',false);
				hadcm3.prop('checked', true);
			}
			else {
				ccsm.prop('checked', true);
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

			cgcm3.prop('checked', true);
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