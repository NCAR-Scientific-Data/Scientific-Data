//Qunit Hello Test
QUnit.test( "hello test", function( assert ) {
assert.ok( 1 == "1", "Passed!" );
});

//Sidebar Tests
QUnit.module("Sidebar");

QUnit.test("New Step Test", function( assert ) {
	newStep();
	assert.strictEqual($("main h1").html(), "What Would You Like To Do?", "New Step Chooser Page should be created");
});

QUnit.test("Create Steps", function( assert ) {
	function makeNewStep(step, numberofsteps) {
		createStep(step, true);
		assert.equal($("aside a").length, numberofsteps, "Number of steps (including new step) should match number of sidebar elements");
	}

	assert.equal($("aside a").length, 1, "Number of steps (including new step) should match number of sidebar elements");
	makeNewStep("Subset", 2);
	makeNewStep("Calculate", 3);
	makeNewStep("Calculate", 4);
	makeNewStep("Results", 5);
	makeNewStep("Subset", 6);
});

// QUnit.test("Delete Steps", function( assert ) {
// 	function deleteCreatedSteps(stepId, numberofsteps) {
// 		$("aside a").removeClass("active");
// 		$(stepId).addClass("active");
// 		deleteStep();
// 		assert.equal($("aside a").length, numberofsteps, "Number of steps (including new step) should match number of sidebar elements");
// 	}

// 	deleteCreatedSteps("#1", 5);
// 	deleteCreatedSteps("#1", 4);
// 	deleteCreatedSteps("#1", 3);
// 	deleteCreatedSteps("#1", 2);
// 	deleteCreatedSteps("#1", 1);
// });