/*
    Title: Analysis Menu Items

    All of the javascript calls for loading analysis pages.
*/

/*
    Functions: Load analysis pages.

        newAggregate - Loads the Aggregate page.
        newUnitConversion - Loads the Unit Conversion page.
        newFilter - Loads the Filter page.
        newPercentile - Loads the Percentile page.
        newBasicOperation - Loads a Basic Operation page.
        newMinMax - Loads a new Min/Max page.
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

function newFilter() {
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

function newBasicOperation() {
    "use strict";
    $("#analysisHTMLLoadSection").empty();
    $("#analysisHTMLLoadSection").load("stepHTML/basicOperation.html");
}

function newMinMax() {
    "use strict";
    $("#analysisHTMLLoadSection").empty();
    $("#analysisHTMLLoadSection").load("stepHTML/minMax.html");
}

