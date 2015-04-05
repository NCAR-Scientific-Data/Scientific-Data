/*global $*/

//Creating/Using Steps----------------------------------------------------------
function newStep() {
    "use strict";
    $("aside a").removeClass("active");
    $("aside a:last").addClass("active");
    $("main").load("chooseStep.html");
}

function insertStep(stepName) {
    "use strict";

    var id = $("aside a").length,
        idfull = "id=\"" + id + "\"",
        onclick = "onclick=\"createStep('" + stepName + "', false, this.id)\"",
        newstep = "<a " + idfull + onclick + ">" + stepName + "</a>";

    $(newstep).insertBefore($("aside a:last"));
    $("aside a").removeClass("active");
    $("#" + id).addClass("active");
}

function createStep(step, isNew, id) {
    "use strict";
    $("main").load(step + ".html");
    if (isNew) {
        insertStep(step, null);
    } else {
        $("aside a").removeClass("active");
        $("#" + id).addClass("active");
    }
}

function deleteStep() {
    "use strict";
    var startId = Number($(".active").attr("id"));

    $("aside a.active").nextAll().each(function () {
        if ($(this).attr('id') !== 0) {
            $(this).attr('id', startId);
            startId += 1;
        }
    });

    $(".active").remove();
    newStep();
}

