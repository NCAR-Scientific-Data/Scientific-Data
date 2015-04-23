/*global $, urlCatalog, addTask*/

function analysis(args, repopulateVals) {
    "use strict";

    var inputs = {
        "var1" : args1,
        "var2" : args2,
    };
    

    addTask("taskName", inputs, repopulateVals);
}

//Parse values from form
function callAnalysis() {
    "use strict";
    
    var repopulateVals = {
        "html" : "stepHTML/taskHTML.html",
        "values" : {
            "#id" : value,
            "#id2" : value2
        }
    }

    analysis(args, repopulateVals);
}