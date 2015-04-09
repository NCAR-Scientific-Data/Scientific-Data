/*global $, location*/
/*
    Function: createWorkflow
    Create a workflow with a unique id.

    See Also:

        <addTask>
*/
function createWorkflow() {
    "use strict";

    $.getJSON("python/createWorkflow", function (results) {
        if (results.uid) {
            localStorage.uid = results.uid;
            $(location).attr("href","workflow-builder.html");
        } else {
            alert("This site is experiencing technical difficulties. Check back later.");
        }
    });
};
