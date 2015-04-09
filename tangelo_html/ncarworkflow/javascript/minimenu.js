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
    $("#HTMLLoadSection").empty();
    $("#HTMLLoadSection").load("stepHTML/subset.html");
    toggleMiniMenu();
    openClosedDrawer();
}

function newAnalysis() {
    "use strict";
    $("#HTMLLoadSection").empty();
    $("#HTMLLoadSection").load("stepHTML/analysis.html");
    toggleMiniMenu();
    openClosedDrawer();
}

function newPlot() {
    "use strict";
    //Load Goes Here
    toggleMiniMenu();
    openClosedDrawer();
}

function newDownload() {
    "use strict";
    //Load Goes Here
    toggleMiniMenu();
    openClosedDrawer();
}
