//Put this file in tangelo_html/ncarworkflow/javascript/analysis
/*global $, addTask, updateTask*/

function analysis(args1, args2, args3, args4, repopulateVals) {
    "use strict";

    var inputs = {
        "var1" : args1,
        "var2" : args2,
        "var3" : args3,
        "var4" : args4
    };

    addTask("taskName", inputs, repopulateVals, "nameOfTaskOutputVariable");
}

//Parse values from form
function callAnalysis() {
    "use strict";

    //For a textbox
    var args1 = $("#inputID1").val();
    //For a radio button
    var args2 = $("input[name='inputName']:checked").val();
    //For a drop down menu
    var args3 = $("#inputID2 option:selected").val();
    
    //If your tasks take other tasks as inputs
    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#inputID3 option:selected").val(),
        args4 = ["Port", selectedNode, allNodes[selectedNode].output];


    //Add repopulate values for textboxes and drop downs
    var repopulateVals = {
        "html" : "stepHTML/taskHTML.html",
        "values" : {
            "#inputID1" : args1,
            "#inputID2" : args3,
        }
    };

    //add repopulate values for radio buttons
    var repopulateValsRadioButton = "input[name='" + args2 + "']";
    var repopulateValsRadioButton2 = "input[name]'" + args4 + "']";

    repopulateVals.values[repopulateValsRadioButton] = true;
    repopulateVals.values[repopulateValsRadioButton2] = true;

    analysis(args1, args2, args3, args4, repopulateVals);
}

function updateAnalysis() {
    "use strict";
    //For a textbox
    var args1 = $("#inputID1").val();
    //For a radio button
    var args2 = $("input[name='inputName']:checked").val();
    //For a drop down menu
    var args3 = $("#inputID2 option:selected").val();
    
    //If your tasks take other tasks as inputs
    var allNodes = JSON.parse(localStorage.nodes),
        selectedNode = $("#inputID3 option:selected").val(),
        args4 = ["Port", selectedNode, allNodes[selectedNode].output];


    //Add repopulate values for textboxes and drop downs
    var repopulateVals = {
        "html" : "stepHTML/taskHTML.html",
        "values" : {
            "#inputID1" : args1,
            "#inputID2" : args3,
        }
    };

    //add repopulate values for radio buttons
    var repopulateValsRadioButton = "input[name='" + args2 + "']";
    var repopulateValsRadioButton2 = "input[name]'" + args4 + "']";

    repopulateVals.values[repopulateValsRadioButton] = true;
    repopulateVals.values[repopulateValsRadioButton2] = true;

    var inputs = {
        "var1" : args1,
        "var2" : args2,
        "var3" : args3,
        "var4" : args4
    };

    updateTask(inputs, repopulateVals);
}

//If your task takes another task as input
function generateNodeSelect() {
    "use strict";
    var nodeDropDown = $("#nodeInputID");

    var nodes = JSON.parse(localStorage.nodes);

    for(var node in nodes) {
        if (node !== "workflowID") {
            var n = nodes[node];
            nodeDropDown.append($("<option></option>").val(node).html(n.name));
        }
    }

    $("#node:first-child").prop("selected", true);
}