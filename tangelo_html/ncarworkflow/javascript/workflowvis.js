/*global window, $, tangelo*/

/*
    File: workflowvis.js
    Visualizes a workflow.
*/


/*
    Function: getIndexMap
    Maps workflow indices to NodeLink indices.

    Parameters:

        workflow - The workflow JSON object.

    Returns:

        A JavaScript object mapping workflow indices to NodeLink indices.

    See Also:

        <formatWorkflow>
*/
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

/*
    Function: generateData
    Generates nodes and links between nodes.

    Parameters:

        workflow - The workflow JSON object.
        indexMap - A map of workflow indices to NodeLink indices.

    Returns:

        A JavaScript object containing 2 properties: *nodes* and *links*.

        *nodes:* A list of nodes. Each node is an object consisting of a node type
        and a node name.

        *links:* A list of links. Each link is an object with a source node index
        and a target node index.


    See Also:

        <formatWorkflow>
*/
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

/*
    Function: listParentsOfTargetNode
    Creates a JavaScript Object mapping nodes to their parent nodes.

    Parameters:

        listOfLinks - a list of links between nodes.

    Returns:

        A JavaScript Object mapping *nodes* to their *parents* by index.

    Example Output:

        (start code)
        {
            6 : [5, 4],
            5 : [3],
            4 : [3],
            3 : [2, 1],
            2 : 0
        }
        (end)

        In this example, the nodes at indices 1 and 0 have no parents. 

    See Also:

        <generateData>

        <formatWorkflow>
*/
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

/*
    Function: assignXValue
    Assigns an initial X value to each node.

    Parameters:

        data - an object containing lists of the nodes and links.
        parentsOfTargetNodes - an object mapping nodes to their parent nodes.

    Returns:

        The number of columns created from the X Values.

    See Also:

        <generateData>

        <listParentsOfTargetNodes>

        <formatWorkflow>
*/
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

/*
    Function: readjustColumns
    Modifies node X-values to make columns more even.

    Parameters:

        data - an object containing lists of the nodes and links.
        numberOfColumns - the number of columns originally created.

    See Also:

        <generateData>

        <assignXValue>

        <formatWorkflow>
*/
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

/*
    Function: assignYValue
    Assigns a Y value to each node.

    Parameters:

        data - an object containing all nodes and links.

    Returns:

        Nothing

    See Also:

        <assignXValue>
        <formatWorkflow>
*/
function assignYValue(data) {
    var nodesInColumns = {},
        height = $("#workflow").height();

    data.nodes.forEach(function (node) {
        if (nodesInColumns.hasOwnProperty(node.x)) {
            nodesInColumns[node.x].push(data.nodes.indexOf(node));
        } else {
            nodesInColumns[node.x] = [data.nodes.indexOf(node)];
        }
    })

    for (nodeX in nodesInColumns) {
        if (nodesInColumns.hasOwnProperty(nodeX)) {
            var nodeList = nodesInColumns[nodeX],
                offset = 0;
            for (var i = 0; i < nodeList.length; i += 1) {
                data.nodes[nodeList[i]].y = (height/nodeList.length/2) + offset;
                offset += height/nodeList.length;
            }
        }
    }
}

/*
    Function: formatWorkflow
    Formats a workflow object into an object easily parsed by nodelink.

    Parameters:

        workflow - The workflow JSON object. Each node is a list consisting of the
        node type, the node name, and a list of indices of child nodes.

    Returns:

        The data object fully formatted for nodelink.

    See Also:

        <getIndexMap>

        <generateData>

        <listParentsOfTargetNodes>

        <assignXValue>

        <readjustColumns>
*/
function formatWorkflow(workflow) {
    "use strict";
    var indexMap = getIndexMap(workflow),
        data = generateData(workflow, indexMap),
        parentsOfTargetNodes = listParentsOfTargetNode(data.links),
        numberOfColumns = assignXValue(data, parentsOfTargetNodes);
    readjustColumns(data, numberOfColumns);
    assignYValue(data);

    return data;
}

/*
    Function: unnamedFunction
    Draws a workflow.

    See Also:

        <formatWorkflow>
*/
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