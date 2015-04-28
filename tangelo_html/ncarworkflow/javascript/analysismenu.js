/*
    Title: Analysis Menu Items

    All of the javascript calls for loading analysis pages.
*/

/*
    Functions: Load analysis pages.

        newAggregate - Loads the Aggregate page.
        newUnitConversion - Loads the Unit Conversion page.
        newCalculateDelta - Loads the Calculate Delta page.
        newPercentile - Loads the Percentile page.
        newThreshold - Loads a Threshold page.
        newClimatology - Loads a Climatology page.
*/

function newAggregate() {
    "use strict";
    $("#analysisHTMLLoadSection").empty();
    $("#analysisHTMLLoadSection").load("stepHTML/aggregate.html");
}

function newUnitConversion() {
    "use strict";
    $("#analysisHTMLLoadSection").empty();
    $("#analysisHTMLLoadSection").load("stepHTML/unitConversion.html");
}

function newCalculateDelta() {
    "use strict";
    $("#analysisHTMLLoadSection").empty();
    $("#analysisHTMLLoadSection").load("stepHTML/filter.html");
}

function newPercentile() {
    "use strict";
    $("#analysisHTMLLoadSection").empty();
    $("#analysisHTMLLoadSection").load("stepHTML/percentile.html");
}

function newThreshold() {
    "use strict";
    $("#analysisHTMLLoadSection").empty();
    $("#analysisHTMLLoadSection").load("stepHTML/threshold.html");
}

function newClimatology() {
    "use strict";
    $("#analysisHTMLLoadSection").empty();
    $("#analysisHTMLLoadSection").load("stepHTML/climatology.html");
}

