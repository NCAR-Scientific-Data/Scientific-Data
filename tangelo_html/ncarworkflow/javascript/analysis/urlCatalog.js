/*
	Variable: urlCatalog
	A Javascript Object that maps OPeNDAP urls to their latest file versions.

	Example:

	If I was retrieving a variable from the first table of a netCDF containing
	the CCSM-Current Global Climate Model and the CRCM Regional Climate Model then
	the entry in the object would be:

	> urlCatalog["crcm.ccsm-current.table1"] = 1;

	See Also:

		<subset>
*/

"use strict";

window.urlCatalog = {};

window.urlCatalog["crcm.ccsm-current.table1"] = 1;
window.urlCatalog["crcm.ccsm-current.table2"] = 4;
window.urlCatalog["crcm.ccsm-current.table3"] = 6;
window.urlCatalog["crcm.ccsm-current.table5"] = 2;

window.urlCatalog["crcm.ccsm-future.table1"] = 1;
window.urlCatalog["crcm.ccsm-future.table2"] = 4;
window.urlCatalog["crcm.ccsm-future.table3"] = 5;
window.urlCatalog["crcm.ccsm-future.table5"] = 2;

window.urlCatalog["crcm.cgcm3-current.table1"] = 7;
window.urlCatalog["crcm.cgcm3-current.table2"] = 4;
window.urlCatalog["crcm.cgcm3-current.table3"] = 7;
window.urlCatalog["crcm.cgcm3-current.table5"] = 2;

window.urlCatalog["crcm.cgcm3-future.table1"] = 2;
window.urlCatalog["crcm.cgcm3-future.table2"] = 4;
window.urlCatalog["crcm.cgcm3-future.table3"] = 7;
window.urlCatalog["crcm.cgcm3-future.table5"] = 3;

window.urlCatalog["crcm.ncep.table1"] = 3;
window.urlCatalog["crcm.ncep.table2"] = 7;
window.urlCatalog["crcm.ncep.table3"] = 10;
window.urlCatalog["crcm.ncep.table5"] = 3;

window.urlCatalog["ecp2.gfdl-current.table1"] = 1;
window.urlCatalog["ecp2.gfdl-current.table2"] = 2;
window.urlCatalog["ecp2.gfdl-current.table3"] = 5;
window.urlCatalog["ecp2.gfdl-current.table5"] = 1;

window.urlCatalog["ecp2.gfdl-future.table1"] = 1;
window.urlCatalog["ecp2.gfdl-future.table2"] = 3;
window.urlCatalog["ecp2.gfdl-future.table3"] = 2;
window.urlCatalog["ecp2.gfdl-future.table5"] = 2;

window.urlCatalog["ecp2.ncep.table1"] = 0;
window.urlCatalog["ecp2.ncep.table2"] = 2;
window.urlCatalog["ecp2.ncep.table3"] = 1;
window.urlCatalog["ecp2.ncep.table5"] = 2;

window.urlCatalog["hrm3.gfdl-current.table1"] = 1;
window.urlCatalog["hrm3.gfdl-current.table2"] = 1;
window.urlCatalog["hrm3.gfdl-current.table3"] = 1;
window.urlCatalog["hrm3.gfdl-current.table5"] = 5;

window.urlCatalog["hrm3.gfdl-future.table1"] = 1;
window.urlCatalog["hrm3.gfdl-future.table2"] = 1;
window.urlCatalog["hrm3.gfdl-future.table3"] = 1;
window.urlCatalog["hrm3.gfdl-future.table5"] = 4;

window.urlCatalog["hrm3.hadcm3-current.table1"] = 4;
window.urlCatalog["hrm3.hadcm3-current.table2"] = 3;
window.urlCatalog["hrm3.hadcm3-current.table3"] = 4;
window.urlCatalog["hrm3.hadcm3-current.table5"] = 3;

window.urlCatalog["hrm3.hadcm3-future.table1"] = 5;
window.urlCatalog["hrm3.hadcm3-future.table2"] = 5;
window.urlCatalog["hrm3.hadcm3-future.table3"] = 6;
window.urlCatalog["hrm3.hadcm3-future.table5"] = 1;

window.urlCatalog["hrm3.ncep.table1"] = 3;
window.urlCatalog["hrm3.ncep.table2"] = 3;
window.urlCatalog["hrm3.ncep.table3"] = 8;
window.urlCatalog["hrm3.ncep.table5"] = 5;

window.urlCatalog["mm5i.ccsm-current.table1"] = 1;
window.urlCatalog["mm5i.ccsm-current.table2"] = 5;
window.urlCatalog["mm5i.ccsm-current.table3"] = 10;
window.urlCatalog["mm5i.ccsm-current.table5"] = 2;

window.urlCatalog["mm5i.ccsm-future.table1"] = 1;
window.urlCatalog["mm5i.ccsm-future.table2"] = 3;
window.urlCatalog["mm5i.ccsm-future.table3"] = 8;
window.urlCatalog["mm5i.ccsm-future.table5"] = 1;

window.urlCatalog["mm5i.hadcm3-current.table1"] = 3;
window.urlCatalog["mm5i.hadcm3-current.table2"] = 3;
window.urlCatalog["mm5i.hadcm3-current.table3"] = 1;
window.urlCatalog["mm5i.hadcm3-current.table5"] = 1;

window.urlCatalog["mm5i.ncep.table1"] = 0;
window.urlCatalog["mm5i.ncep.table2"] = 4;
window.urlCatalog["mm5i.ncep.table3"] = 3;
window.urlCatalog["mm5i.ncep.table5"] = 3;

window.urlCatalog["rcm3.cgcm3-current.table1"] = 4;
window.urlCatalog["rcm3.cgcm3-current.table2"] = 2;
window.urlCatalog["rcm3.cgcm3-current.table3"] = 5;
window.urlCatalog["rcm3.cgcm3-current.table5"] = 1;

window.urlCatalog["rcm3.cgcm3-future.table1"] = 4;
window.urlCatalog["rcm3.cgcm3-future.table2"] = 2;
window.urlCatalog["rcm3.cgcm3-future.table3"] = 5;
window.urlCatalog["rcm3.cgcm3-future.table5"] = 1;

window.urlCatalog["rcm3.gfdl-current.table1"] = 3;
window.urlCatalog["rcm3.gfdl-current.table2"] = 3;
window.urlCatalog["rcm3.gfdl-current.table3"] = 5;
window.urlCatalog["rcm3.gfdl-current.table5"] = 1;

window.urlCatalog["rcm3.gfdl-future.table1"] = 3;
window.urlCatalog["rcm3.gfdl-future.table2"] = 3;
window.urlCatalog["rcm3.gfdl-future.table3"] = 5;
window.urlCatalog["rcm3.gfdl-future.table5"] = 1;

window.urlCatalog["rcm3.ncep.table1"] = 3;
window.urlCatalog["rcm3.ncep.table2"] = 5;
window.urlCatalog["rcm3.ncep.table3"] = 7;
window.urlCatalog["rcm3.ncep.table5"] = 0;

window.urlCatalog["wrfg.ccsm-current.table1"] = 3;
window.urlCatalog["wrfg.ccsm-current.table2"] = 1;
window.urlCatalog["wrfg.ccsm-current.table3"] = 6;
window.urlCatalog["wrfg.ccsm-current.table5"] = 3;

window.urlCatalog["wrfg.ccsm-future.table1"] = 3;
window.urlCatalog["wrfg.ccsm-future.table2"] = 1;
window.urlCatalog["wrfg.ccsm-future.table3"] = 6;
window.urlCatalog["wrfg.ccsm-future.table5"] = 1;

window.urlCatalog["wrfg.cgcm3-current.table1"] = 1;
window.urlCatalog["wrfg.cgcm3-current.table2"] = 1;
window.urlCatalog["wrfg.cgcm3-current.table3"] = 6;
window.urlCatalog["wrfg.cgcm3-current.table5"] = 1;

window.urlCatalog["wrfg.cgcm3-future.table1"] = 1;
window.urlCatalog["wrfg.cgcm3-future.table2"] = 2;
window.urlCatalog["wrfg.cgcm3-future.table3"] = 7;
window.urlCatalog["wrfg.cgcm3-future.table5"] = 1;

window.urlCatalog["wrfg.ncep.table1"] = 3;
window.urlCatalog["wrfg.ncep.table2"] = 2;
window.urlCatalog["wrfg.ncep.table3"] = 5;
window.urlCatalog["wrfg.ncep.table5"] = 4;