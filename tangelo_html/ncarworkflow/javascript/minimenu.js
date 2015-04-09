$( document ).ready(function() {
  		
});

function toggleMiniMenu() {
	"use strict";
	$(".miniMenuOption").toggle("fast");
}

function newSubset() {
  	$("#StepMaker").empty();
	$("#StepMaker").load("Subset.html")
	console.log("Stepmaker:", $("#StepMaker"));
	
}

function newAnalysis() {
	$("#StepMaker").empty();
	$("#StepMaker").load("Analysis.html")
}

function newPlot() {

}

function newDownload() {

}

