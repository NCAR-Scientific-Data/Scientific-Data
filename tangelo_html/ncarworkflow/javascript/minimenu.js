/*global $*/
/*
    Title: Mini Menu
    Functions pertaining to the mini-menu in the top right corner of the workflow builder.
*/

/*
    Function: toggleMiniMenu

    Toggles the mini menu's display.
*/
function toggleMiniMenu() {
    "use strict";
    $(".miniMenuOption").toggle("fast");
}

/*
    Function: openClosedDrawer

    If the edit drawer is closed, it is opened.
*/
function openClosedDrawer() {
    "use strict";
    if ($("#StepMaker").height() <= 20) {
        $("[id^='tangelo-drawer-icon-']").trigger("click");
    }
}

/* 
    Functions: Load Basic Pages

    newSubset - Loads a Subset page.
    newAnalysis - Loads an Analysis page.
    newPlot - Loads a Plot page.
*/

function newSubset() {
    "use strict";
    $("#analysisWrapper").empty();
    $("#analysisWrapper").load("stepHTML/subset.html");
    toggleMiniMenu();
    openClosedDrawer();
}

function newAnalysis() {
    "use strict";
    $("#analysisWrapper").empty();
    $("#analysisWrapper").load("stepHTML/analysis.html");
    toggleMiniMenu();
    openClosedDrawer();
}

function newPlot() {
    "use strict";
    $("#analysisWrapper").empty();
    $("#analysisWrapper").load("stepHTML/plot.html");
    toggleMiniMenu();
    openClosedDrawer();
}
