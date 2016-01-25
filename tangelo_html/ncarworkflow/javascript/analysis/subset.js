/*global $, addTask, updateTask*/

/*
    Title: Subset
*/

/*
    Function: subset
    Creates the inputs and calls addTask.

    See Also:

        <urlCatalog>
*/
function subset(simulationType, variable, swlat, swlon, nelat, nelon, timestart, timeend, rcm, gcm, repopulateVals) {
    "use strict";

    var basicString = "http://tds.ucar.edu/thredds/dodsC/narccap.",
        modelString = rcm + "." + gcm + simulationType + "." + variable.substring(0,6),
        version = window.urlCatalog[modelString];

        modelString += variable.substring(6);

        if (version === 0) {
            version = ".aggregation";
        } else {
            version = "." + String(version) + ".aggregation";
        }


    var url = basicString + modelString + version;

    var inputs = {
        "url" : url,
        "variable" : variable.substring(7),
        "swlat" : swlat,
        "swlon" : swlon,
        "nelat" : nelat,
        "nelon" : nelon,
        "startdate" : timestart,
        "enddate" : timeend
    };

    //inputs = JSON.stringify(inputs);

    //addTask("taskSubset", inputs, repopulateVals, "subset");
}

/*
    Function: callSubset
    Parse the form and creates the repopulation values object.
*/
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
        gcm = $("input[name='gcm']:checked").val(),
        variableSelector = "input[name='variable'][value='" + variable+ "']",
        rcmSelector = "input[name='rcm'][value='" + rcm + "']",
        gcmSelector = "input[name='gcm'][value='" + gcm + "']",
        repopulateVals;

    repopulateVals = {
        "html" : "stepHTML/subset.html",
        "values" : {
            "#simulationType" : simulationType,
            "#swlat" : swlat,
            "#swlon" : swlon,
            "#nelat" : nelat,
            "#nelon" : nelon,
            "#startYear" :  $("#startYear option:selected").val(),
            "#startMonth" : $("#startMonth option:selected").val(),
            "#startDay" : $("#startDay option:selected").val(),
            "#endYear" : $("#endYear option:selected").val(),
            "#endMonth" : $("#endMonth option:selected").val(),
            "#endDay" : $("#endDay option:selected").val(),
        }
        
    };

    repopulateVals.values[rcmSelector] = true;
    repopulateVals.values[gcmSelector] = true;
    repopulateVals.values[variableSelector] = true;


    subset(simulationType, variable, swlat, swlon, nelat, nelon, timestart, timeend, rcm, gcm, repopulateVals);
}

/*
    Function: updateSubset()
    Performs the same steps as callSubset() and subset(), except it updates an existing node instead of creating a new node.
*/
function updateSubset() {
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
        gcm = $("input[name='gcm']:checked").val(),
        variableSelector = "input[name='variable'][value='" + variable+ "']",
        rcmSelector = "input[name='rcm'][value='" + rcm + "']",
        gcmSelector = "input[name='gcm'][value='" + gcm + "']",
        repopulateVals;

    repopulateVals = {
        "html" : "stepHTML/subset.html",
        "values" : {
            "#simulationType" : simulationType,
            "#swlat" : swlat,
            "#swlon" : swlon,
            "#nelat" : nelat,
            "#nelon" : nelon,
            "#startYear" :  $("#startYear option:selected").val(),
            "#startMonth" : $("#startMonth option:selected").val(),
            "#startDay" : $("#startDay option:selected").val(),
            "#endYear" : $("#endYear option:selected").val(),
            "#endMonth" : $("#endMonth option:selected").val(),
            "#endDay" : $("#endDay option:selected").val(),
        }
        
    };

    repopulateVals.values[rcmSelector] = true;
    repopulateVals.values[gcmSelector] = true;
    repopulateVals.values[variableSelector] = true;

    var basicString = "http://tds.ucar.edu/thredds/dodsC/narccap.",
        modelString = rcm + "." + gcm + simulationType + "." + variable.substring(0,6),
        version = window.urlCatalog[modelString];

        modelString += variable.substring(6);

        if (version === 0) {
            version = ".aggregation";
        } else {
            version = "." + String(version) + ".aggregation";
        }


    var url = basicString + modelString + version;

    var inputs = {
        "url" : url,
        "variable" : variable.substring(7),
        "swlat" : swlat,
        "swlon" : swlon,
        "nelat" : nelat,
        "nelon" : nelon,
        "startdate" : timestart,
        "enddate" : timeend
    };


    updateTask(inputs, repopulateVals);
}

/*
    Function: changeDateRange
    Changes the date range available for subset based on the simulation type.

    Parameters:

    simulationType - a string representing the simulation type. Can either be "ncep", "-current", or "-future".
*/
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
        startYearDropDown.append($("<option></option>").val(i).html(i.toString()));
        endYearDropDown.append($("<option></option>").val(i).html(i.toString()));
    }

    $("#endYear option:last-child").prop("selected", true);
}

/*
    Function: changeGCM
    Change the Global Climate Model input options based on the simulation type and Regional Climate Model.

    Parameters:

    simulationType -  A string with the value of the simulation type, either "ncep", "-current", or "-future".
    rcm - A string with the value of the Regional Climate Model, either "ccsm", "cgcm3", "gfdl", or "hadcm3".
*/
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
        $("#none").attr("disabled", false);

        $("#none").prop("checked", true);
    } else {
        if (rcm === "crcm") {
            ccsm.attr("disabled", false);
            cgcm3.attr("disabled", false);

            cgcm3.prop("checked", true);
        } else if (rcm === "ecp2") {

            gfdl.attr("disabled", false);

            gfdl.prop("checked", true);

        } else if (rcm === "hrm3") {

            gfdl.attr("disabled", false);
            hadcm3.attr("disabled", false);

            gfdl.prop("checked", true);

        } else if (rcm === "mm5i") {

            ccsm.attr("disabled", false);

            if (simulationType === "-current") {

                hadcm3.attr("disabled", false);
                hadcm3.prop("checked", true);

            } else {

                ccsm.prop("checked", true);

            }
        } else if (rcm === "rcm3") {

            gfdl.attr("disabled", false);
            cgcm3.attr("disabled", false);

            gfdl.prop("checked", true);

        } else if (rcm === "wrfg") {

            ccsm.attr("disabled", false);
            cgcm3.attr("disabled", false);

            cgcm3.prop("checked", true);
        }
    }
}

/*
    Function: changeBasedOnSim
    Change certain input values based on the Simulation type.

    See Also:

        <changeDateRange>
        
        <changeGCM>
*/
function changeBasedOnSim() {
    "use strict";

    var simulationType = $("#simulationType option:selected").val(),
        rcm = $("input[name='rcm']:checked").val();

    changeDateRange(simulationType);
    changeGCM(simulationType, rcm);
}

/*
    Function: changeBasedOnRCM
    Change certain input values based on the Regional Climate Model.

    See Also:
        <changeGCM>
*/
function changeBasedOnRCM() {
    "use strict";

    var simulationType = $("#simulationType option:selected").val(),
        rcm = $("input[name='rcm']:checked").val();

    changeGCM(simulationType, rcm);
}