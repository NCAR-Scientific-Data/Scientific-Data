/*global window, $, tangelo*/

function getIndexMap(workflow) {
    "use strict";
    var indexMap = {},
        nodeIndexForNodeLink = 0;

    workflow.forEach(function (nodeProperties) {
        var nodeIndex = nodeProperties[1];
        indexMap[nodeIndex] = nodeIndexForNodeLink;
        nodeIndexForNodeLink += 1;
    });
    return indexMap;
}

function generateData(workflow, indexMap) {
    "use strict";
    var data = { nodes: [], links: []};

    workflow.forEach(function (nodeProperties) {
        var nodeType = nodeProperties[0],
            nodeIndex = nodeProperties[1],
            nodeLinks = nodeProperties[2],
            nodeName = nodeProperties[0] + nodeProperties[1],
            sourceIndex;

        data.nodes.push({type: nodeType, name: nodeName});

        sourceIndex = nodeIndex;

        for (var i = 0; i < nodeLinks.length; i += 1) {
            var linkedNodeIndex = nodeLinks[i];
            if (indexMap[linkedNodeIndex]) {
                var sourceNode = indexMap[sourceIndex],
                    targetNode = indexMap[linkedNodeIndex];

                data.links.push({source: sourceNode, target: targetNode});
            }
        }
    });
    return data;

}

function listParentsOfTargetNode(listOfLinks) {
    "use strict";
    var parentsOfTargetNodes = {};

    listOfLinks.forEach(function (linkDictionary) {
        var sourceNode = linkDictionary.source,
            targetNode = linkDictionary.target;

        if (parentsOfTargetNodes.hasOwnProperty(targetNode)) {

            parentsOfTargetNodes[targetNode].push(sourceNode);

        } else {

            parentsOfTargetNodes[targetNode] = [sourceNode];

        }
    });
    return parentsOfTargetNodes;
}

function assignXValue(data, parentsOfTargetNodes) {
    "use strict";

    var width = $("#workflow").width(),
        numberOfColumns = Object.keys(parentsOfTargetNodes).length + 1,
        columnSize = width / numberOfColumns,
        x = columnSize / 2;

    for (var targetNode in parentsOfTargetNodes) {

        if (parentsOfTargetNodes.hasOwnProperty(targetNode)) {
            
            var lengthOfParentsList = parentsOfTargetNodes[targetNode].length,
                listOfNodesToChangeX = parentsOfTargetNodes[targetNode];
            for (var i = 0; i < lengthOfParentsList; i += 1) {
                data.nodes[listOfNodesToChangeX[i]].x = x;
            }

            x += columnSize;
        }
    }

    data.nodes[data.nodes.length - 1].x = x;

    return numberOfColumns;
}

function readjustColumns(data, numberOfColumns) {
    "use strict";
    var currentColumns = [],
        numberOfActualColumns,
        actualColumnSize,
        actualColumns,
        actualX,
        columnMap = {},
        width = $("#workflow").width();

    data.nodes.forEach(function (node) {
        if (currentColumns.indexOf(node.x) < 0) {

            currentColumns.push(node.x);

        }
    });

    currentColumns.sort(function (a, b) {
        return a - b;
    });

    numberOfActualColumns = currentColumns.length;

    if (numberOfColumns !== numberOfActualColumns) {

        actualColumnSize = width / numberOfActualColumns;
        actualX = actualColumnSize / 2;

        actualColumns = currentColumns.map(function (value, index) {
            if (index === 0) {
                return actualX;
            }
            actualX += actualColumnSize;
            return actualX;
        });

        for (var i = 0; i < actualColumnSize; i += 1) {

            var oldx = currentColumns[i],
                newx = actualColumns[i];

            columnMap[oldx] = newx;
        }

        data.nodes.forEach(function (node) {
            node.x = columnMap[node.x];
        });
    }
}

function formatWorkflow(workflow) {
    "use strict";
    var indexMap = getIndexMap(workflow),
        data = generateData(workflow, indexMap),
        parentsOfTargetNodes = listParentsOfTargetNode(data.links),
        numberOfColumns = assignXValue(data, parentsOfTargetNodes);
    readjustColumns(data, numberOfColumns);

    return data;
}

window.onload = function () {
    "use strict";
    var url = "python/workflowTwo";

    $.getJSON(url, function (results) {
        if (results.workflow) {
            var data = formatWorkflow(results.workflow);

            $("#workflow").nodelink({
                data: data,
                nodeCharge: tangelo.accessor({value: -10000}),
                linkSource: tangelo.accessor({field: "source"}),
                linkTarget: tangelo.accessor({field: "target"}),
                nodeColor: tangelo.accessor({field: "type"}),
                nodeLabel: tangelo.accessor({field: "name"})
            });
        }
    });
};