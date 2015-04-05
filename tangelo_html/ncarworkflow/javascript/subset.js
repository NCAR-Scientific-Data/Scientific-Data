/*global $, localStorage*/

function subset(simulationType, variable, swlat, swlon, nelat, nelon, timestart, timeend, rcm, gcm) {
    "use strict";
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

    var url = "python/grabNetcdf?" + simulationType + variable + swlat + swlon + nelat + nelon + timestart + timeend + rcm + gcm;

    $("<p>Subsetting. Please Wait.</p>").insertAfter($(".form-inline"));

    $.getJSON(url, function (data) {
        if (data.subset) {
            $("p").html("Subset Succesful!");
            localStorage.subset = data.subset;

        } else {
            $("p").html("Subset Failed.<br>" + data.error);
            localStorage.subset = "";
        }
    });
}

function callSubset() {
    "use strict";
    var simulationType = $("#simulationType option:selected").val(),
        variable = $("input[name='variable']:checked").val(),
        swlat = $("#swlat").val(),
        swlon = $("#swlon").val(),
        nelat = $("#nelat").val(),
        nelon = $("#nelon").val(),
        timestart = $("#startYear option:selected").val() + "-" + $("#startMonth option:selected").val() + "-" + $("#startDay option:selected").val(),
        timeend = $("#endYear option:selected").val() + "-" + $("#endMonth option:selected").val() + "-" + $("#endDay option:selected").val(),
        rcm = $("input[name='rcm']:checked").val(),
        gcm = $("input[name='gcm']:checked").val();

    subset(simulationType, variable, swlat, swlon, nelat, nelon, timestart, timeend, rcm, gcm);
}

function changeDateRange(simulationType) {
    "use strict";
    var start, end, i,
        startYearDropDown = $("#startYear"),
        endYearDropDown = $("#endYear");

    if (simulationType === "ncep") {
        start = 1979;
        end = 2004;
    } else if (simulationType === "-current") {
        start = 1970;
        end = 2000;
    } else {
        start = 2040;
        end = 2070;
    }

    startYearDropDown.empty();
    endYearDropDown.empty();

    for (i = start; i <= end; i += 1) {
        startYearDropDown.append($('<option></option>').val(i).html(i.toString()));
        endYearDropDown.append($('<option></option>').val(i).html(i.toString()));
    }

    $("#endYear option:last-child").prop("selected", true);
}

function changeGCM(simulationType, rcm) {
    "use strict";

    var ccsm = $("#ccsm"),
        cgcm3 = $("#cgcm3"),
        gfdl = $("#gfdl"),
        hadcm3 = $("#hadcm3");

    $("input[name='gcm']").each(function () {
        $(this).attr("disabled", true);
    });

    if (simulationType === "ncep") {
        $("#none").attr('disabled', false);

        $("#none").prop('checked', true);
    } else {
        if (rcm === "crcm") {
            ccsm.attr('disabled', false);
            cgcm3.attr('disabled', false);

            cgcm3.prop('checked', true);
        } else if (rcm === "ecp2") {

            gfdl.attr('disabled', false);

            gfdl.prop('checked', true);

        } else if (rcm === "hrm3") {

            gfdl.attr('disabled', false);
            hadcm3.attr('disabled', false);

            gfdl.prop('checked', true);

        } else if (rcm === "mm5i") {

            ccsm.attr('disabled', false);

            if (simulationType === "-current") {

                hadcm3.attr('disabled', false);
                hadcm3.prop('checked', true);

            } else {

                ccsm.prop('checked', true);

            }
        } else if (rcm === "rcm3") {

            gfdl.attr('disabled', false);
            cgcm3.attr('disabled', false);

            gfdl.prop('checked', true);

        } else if (rcm === "wrfg") {

            ccsm.attr('disabled', false);
            cgcm3.attr('disabled', false);

            cgcm3.prop('checked', true);
        }
    }
}

function changeBasedOnSim() {
    "use strict";

    var simulationType = $("#simulationType option:selected").val(),
        rcm = $("input[name='rcm']:checked").val();

    changeDateRange(simulationType);
    changeGCM(simulationType, rcm);
}

function changeBasedOnRCM() {
    "use strict";

    var simulationType = $("#simulationType option:selected").val(),
        rcm = $("input[name='rcm']:checked").val();

    changeGCM(simulationType, rcm);
}