/*global $*/

function toggleMiniMenu() {
    "use strict";
    $(".miniMenuOption").toggle("fast");
}

function openClosedDrawer() {
    "use strict";
    if ($("#StepMaker").height() <= 20) {
        $("[id^='tangelo-drawer-icon-']").trigger("click");
    }
}

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
