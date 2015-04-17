/*global $, location*/
/*
    Function: createWorkflow
    Create a workflow with a unique id.

    See Also:

        <addTask>
*/
function createWorkflow() {
    "use strict";

    var args = {
        "function" : "createWorkflow",
        "workflowID" : " ",
        "args" : "{}"
    }

    $.getJSON("python/updateWorkflow", args, function (results) {
        if (results.uid) {
            localStorage.uid = results.uid;
            localStorage.nodes = JSON.stringify({ "workflowID" : results.uid});
            $(location).attr("href","workflow-builder.html");
        } else {
            alert("This site is experiencing technical difficulties. Check back later.");
        }
    });
};
