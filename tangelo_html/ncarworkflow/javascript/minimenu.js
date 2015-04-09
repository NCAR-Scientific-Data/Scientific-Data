function toggleMiniMenu() {
	"use strict";
	$(".miniMenuOption").toggle("fast");
}

function newSubset() {
	"use strict";
  	$("#StepMaker").empty();
	$("#StepMaker").load("Subset.html")
	//console.log("Stepmaker:", $("#StepMaker"));
}

function newAnalysis() {
	"use strict";
	$("#StepMaker").empty();
	$("#StepMaker").load("Analysis.html")
}

function newPlot() {
	"use strict";
}

function newDownload() {
	"use strict";
}
