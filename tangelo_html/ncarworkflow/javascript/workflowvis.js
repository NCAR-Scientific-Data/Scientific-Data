/*global window, $*/

window.onload = function () {
    "use strict";
    var url = "python/workflowTwo";

    $.getJSON(url, function (results) {
        if (results.workflow) {
            var workflow = results.workflow,
                indexMap = {},
                i = 0,
                data = { nodes: [], links: []},
                width = $("#workflow").width(),
                height = $("#workflow").height(),
                targetParents = {},
                numberOfColumns,
                columnSize,
                x,
                target;

            workflow.forEach(function (list) {
                var oldIndex = list[1];
                indexMap[oldIndex] = i;
                i += 1;
            });

            workflow.forEach(function (list) {
                data.nodes.push({type: list[0], name: list[0] + list[1]});
                list[2].forEach(function (index) {
                    var sourceIndex = list[1];
                    if (indexMap[index]) {
                        data.links.push({source: indexMap[sourceIndex], target: indexMap[index]});
                    }
                });
            });

            data.links.forEach(function (dict) {
                var sourceNode = dict.source,
                    targetNode = dict.target;

                if (targetParents[targetNode]) {
                    targetParents[targetNode].push(sourceNode);
                } else {
                    targetParents[targetNode] = [sourceNode];
                }

            });

            numberOfColumns = Object.keys(targetParents).length + 1;
            columnSize = width / numberOfColumns;
            x = columnSize / 2;

            for (target in targetParents) {
                if (!$.isEmptyObject(target)) {
                    targetParents[target].forEach(function (index) {
                        data.nodes[index].x = x;
                    });
                    x += columnSize;
                }
            }

            data.nodes[data.nodes.length - 1].x = x;

            var currentColumns = [];
            data.nodes.forEach( function(node) {
                if(currentColumns.indexOf(node.x) < 0)
                {
                    currentColumns.push(node.x);
                }
            });

            currentColumns.sort(function (a, b) {
                return a-b;
            });

            var numberOfActualColumns = currentColumns.length;
            
            if (numberOfColumns != numberOfActualColumns) {

                var actualColumnSize = width/numberOfActualColumns;
                var actualX = actualColumnSize/2;

                var actualColumns = currentColumns.map( function(value, index) {
                    if( index == 0) {
                        return actualX;
                    }
                    actualX += actualColumnSize;
                    return actualX;
                });

                var columnMap = {};
                for(var i = 0, len=actualColumnSize; i < actualColumnSize; i++)
                {
                    var oldx = currentColumns[i];
                    var newx = actualColumns[i];
                    columnMap[oldx] = newx;
                }

                data.nodes.forEach( function(node) {
                        node.x = columnMap[node.x];
                });
            }   



            $("#workflow").nodelink({
                data: data,
                nodeCharge: tangelo.accessor({value: -10000}),
                linkSource: tangelo.accessor({field: "source"}),
                linkTarget: tangelo.accessor({field: "target"}),
                nodeColor: tangelo.accessor({field: "type"}),
                nodeLabel: tangelo.accessor({field: "name"}),
            });
        }
    });
};