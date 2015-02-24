//Modifying Dates
QUnit.module("Dates");
QUnit.test("updateDate", function( assert ) {
	function datesUpdatedBySim(simtype, expectedStart, expectedEnd) {
		var expectedArray = [];
		var returnedArrayStart = [];
		var returnedArrayEnd = [];
		for (i = expectedStart; i <= expectedEnd; i++) {
			expectedArray.push(i.toString());
		}

		changeDateRange(simtype);

		$("#startYear > option").each(function() {
			returnedArrayStart.push($(this).val());
		});

		$("#endYear > option").each(function() {
			returnedArrayEnd.push($(this).val());
		});

		var message = "Sim <" + simtype + "> should yield " + "[" + expectedArray.toString() + "]";

		assert.deepEqual(returnedArrayStart, expectedArray, message);
		assert.deepEqual(returnedArrayEnd, expectedArray, message);
	}

	datesUpdatedBySim("ncep", 1979, 2004);
	datesUpdatedBySim("-current", 1970, 2000);
	datesUpdatedBySim("-future", 2040, 2070);
});

QUnit.test("defaultDate", function( assert ) {
	function dateDefaults(simtype, expectedStart, expectedEnd) {
		changeDateRange(simtype);

		assert.equal($("#startYear option:selected").val(), expectedStart, "Start Year == Expected Start Year");
		assert.equal($("#endYear option:selected").val(), expectedEnd, "End Year == Expected End Year");
	}

	dateDefaults("ncep", 1979, 2004);
	dateDefaults("-current", 1970, 2000);
	dateDefaults("-future", 2040, 2070);
});

QUnit.module("GCM");
QUnit.test("UpdateGCM", function( assert ) {
	function gcmUpdated(simtype, rcm, expected) {
		changeGCM(simtype, rcm);
		var enabled = [];

		$("input[name='gcm']").each(function() {
			if ($(this).attr("disabled") !== "disabled") {
				enabled.push($(this).attr("id"));
			}
		})

		var message = "Sim <" + simtype + "> and RCM <" + rcm + "> should yield ";

		assert.deepEqual(enabled, expected, message + "[" + expected.toString() + "]");
	}

	gcmUpdated("ncep", "crcm", ["none"]);
	gcmUpdated("ncep", "ecp2", ["none"]);
	gcmUpdated("ncep", "hrm3", ["none"]);
	gcmUpdated("ncep", "mm5i", ["none"]);
	gcmUpdated("ncep", "rcm3", ["none"]);
	gcmUpdated("ncep", "wrfg", ["none"]);

	gcmUpdated("-current", "crcm", ["cgcm3", "ccsm"]);
	gcmUpdated("-current", "ecp2", ["gfdl"]);
	gcmUpdated("-current", "hrm3", ["gfdl", "hadcm3"]);
	gcmUpdated("-current", "mm5i", ["hadcm3", "ccsm"]);
	gcmUpdated("-current", "rcm3", ["gfdl", "cgcm3"]);
	gcmUpdated("-current", "wrfg", ["cgcm3", "ccsm"]);

	gcmUpdated("-future", "crcm", ["cgcm3", "ccsm"]);
	gcmUpdated("-future", "ecp2", ["gfdl"]);
	gcmUpdated("-future", "hrm3", ["gfdl", "hadcm3"]);
	gcmUpdated("-future", "mm5i", ["ccsm"]);
	gcmUpdated("-future", "rcm3", ["gfdl", "cgcm3"]);
	gcmUpdated("-future", "wrfg", ["cgcm3", "ccsm"]);
});

QUnit.test("DefaultGCM", function( assert ) {
	function defaults(simtype, rcm, expected) {
		changeGCM(simtype, rcm);
		var message = "Default value should be " + expected + " given Sim <" + simtype + "> and RCM <" + rcm + ">";
		assert.strictEqual($("input[name='gcm']:checked").attr("id"), expected, message);
	}

	defaults("ncep", "crcm", "none");
	defaults("ncep", "ecp2", "none");
	defaults("ncep", "hrm3", "none");
	defaults("ncep", "mm5i", "none");
	defaults("ncep", "rcm3", "none");
	defaults("ncep", "wrfg", "none");

	defaults("-current", "crcm", "cgcm3");
	defaults("-current", "ecp2", "gfdl");
	defaults("-current", "hrm3", "gfdl");
	defaults("-current", "mm5i", "hadcm3");
	defaults("-current", "rcm3", "gfdl");
	defaults("-current", "wrfg", "cgcm3");

	defaults("-future", "crcm", "cgcm3");
	defaults("-future", "ecp2", "gfdl");
	defaults("-future", "hrm3", "gfdl");
	defaults("-future", "mm5i", "ccsm");
	defaults("-future", "rcm3", "gfdl");
	defaults("-future", "wrfg", "cgcm3");
});

//Subsetting Module
QUnit.module("Subset");
QUnit.test("subset", function( assert ) {
	expect(0);
});