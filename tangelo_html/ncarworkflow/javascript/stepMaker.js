//Creating/Using Steps----------------------------------------------------------
function newStep() {
	$("aside a").removeClass("active");
	$("aside a:last").addClass("active");
	$("main").load("chooseStep.html");
}

function createStep(step, isNew, id) {
	$("main").load(step + ".html");
	if(isNew)
	{
		insertStep(step, null);
	}
	else
	{
		$("aside a").removeClass("active");
		$("#"+id).addClass("active");
	}	
}

function deleteStep() {
	var startId = Number($(".active").attr("id"));
	$("aside a.active").nextAll().each(function (index) {
		if($(this).attr('id') != 0)
		{
			$(this).attr('id', startId);
			startId+= 1;
		}
	});
	$(".active").remove();
	newStep();
}

function insertStep(stepName, stepValues) {
	var id= $("aside a").length;
	var idfull = "id=\"" + id +"\"";
	var onclick = "onclick=\"createStep('" + stepName + "', false, this.id)\"";
	
	var newstep = "<a " + idfull + onclick + ">" + stepName + "</a>";
	$(newstep).insertBefore($("aside a:last"));
	$("aside a").removeClass("active");
	$("#" + id).addClass("active");
}