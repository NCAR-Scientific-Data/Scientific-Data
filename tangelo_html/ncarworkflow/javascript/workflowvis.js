/*global window, $, tangelo, confirm, alert*/

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
        listOfNodeIndices = [];

    workflow.forEach(function (nodeProperties) {
        var nodeIndex = nodeProperties[1];
        listOfNodeIndices.push(nodeIndex);
    });

    if (listOfNodeIndices.length > 1) {
        listOfNodeIndices.sort();

        var lengthOfList = listOfNodeIndices.length,
            minNode = listOfNodeIndices[0],
            maxNode = listOfNodeIndices[lengthOfList-1],
            minIndex = 0,
            maxIndex = lengthOfList-1;

        for (var i = 0; i < lengthOfList; i += 1) {
            var node = listOfNodeIndices[i];

            indexMap[node] = (node - minNode) / (maxNode - minNode) * (maxIndex - minIndex) + minIndex;
        }
    } else {
        indexMap[listOfNodeIndices[0]] = 0;
    }

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
    var data = { nodes: [workflow.length], links: []},
        bfsList = [workflow.length];

    for (var i = 0; i < workflow.length; i += 1) {
        bfsList[i] = [];
    }

    workflow.forEach(function (nodeProperties) {
        var nodeType = nodeProperties[0],
            nodeIndex = nodeProperties[1],
            nodeLinks = nodeProperties[2],
            nodeUID = nodeProperties[3],
            nodeName = nodeType + nodeIndex,
            sourceIndex;

        data.nodes[indexMap[nodeIndex]] = {type: nodeType, name: nodeName, uid: nodeUID}

        sourceIndex = nodeIndex;

        for (var i = 0; i < nodeLinks.length; i += 1) {
            var linkedNodeIndex = nodeLinks[i];
            if (indexMap[linkedNodeIndex]) {
                var sourceNode = indexMap[sourceIndex],
                    targetNode = indexMap[linkedNodeIndex];

                bfsList[sourceNode].push(targetNode);
                

                data.links.push({source: sourceNode, target: targetNode});
            }
        }
    });

    return [data, bfsList];
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
function assignXValue(data, bfsList) {
    "use strict";
    console.log(bfsList);

    var width = $("#workflow").width(),
        numberOfColumns = bfsList.length;

    var columnSize = width / numberOfColumns,
        x = columnSize / 2,
        startbranchx = x + columnSize;

    for (var i = 0; i < bfsList.length; i += 1) {
        var tmpx = startbranchx;
        if (data.nodes[i].x) {
            tmpx = data.nodes[i].x + columnSize;
        }
        console.log(tmpx);
        for (var j = 0; j < bfsList[i].length; j += 1) {
            data.nodes[bfsList[i][j]].x = tmpx;
        }
    }

    for (var i = 0; i < bfsList.length; i += 1) {
        if (data.nodes[i].x) {
            
        } else {
            data.nodes[i].x = x;
        }
        console.log(data.nodes[i].x);
    }

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
function assignYValue(data, bfs) {
    "use strict";
    var height = $("#workflow").height();

    for (var i = 0; i < bfs.length; i++) {
        var numRows = bfs[i].length,
            rowHeight = height / numRows,
            y = rowHeight / 2;

        for (var j = 0; j < numRows; j++) {
            data.nodes[bfs[i][j]].y = y;
            y += rowHeight;
        }
    }

    var missedList = [];
    for (var i = 0; i < bfs.length; i += 1) {
        if (!data.nodes[i].hasOwnProperty("y")) {
            missedList.push(i);
        }
    }

    var numRows = missedList.length,
        rowHeight = height / numRows,
        y = rowHeight / 2;
    for (var i = 0; i < missedList.length; i += 1) {
        data.nodes[missedList[i]].y = y;
        y += rowHeight;
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
    if (workflow.length === 0) {
        return { nodes : [], links : []};
    }

    var indexMap = getIndexMap(workflow),
        dataAndBFS = generateData(workflow, indexMap),
        data = dataAndBFS[0],
        bfs = dataAndBFS[1],
        numberOfColumns = assignXValue(data, bfs);
    readjustColumns(data, numberOfColumns);
    assignYValue(data, bfs);

    return data;
}

/*
    Function: addTask
    Run and then draw a workflow.

    See Also:

        <formatWorkflow>
*/
function addTask(task_Type, links, repopulateVals, outputName) {
    "use strict";

    var url = "python/updateWorkflow",
        stuffToPass = {
            "function" : "addTask",
            "workflowID" : localStorage.uid,
            "args" : JSON.stringify([task_Type, JSON.stringify(links)])
        };

    $.getJSON(url, stuffToPass, function (results) {
        if (results.result) {
            $("[id^='tangelo-drawer-icon-']").trigger("click");
            $("#analysisWrapper").empty();
            $("#analysisWrapper").html("<h1>NCAR Scientific Workflows</h1>");
            
            var data = formatWorkflow(results.workflow),
                tid = results.taskID,
                nodes = JSON.parse(localStorage.nodes);

            var n = data.nodes;

            for (var i = 0; i < n.length; i += 1) {
                var taskid = n[i].uid,
                    name = n[i].name;

                if (nodes.hasOwnProperty(taskid)) {
                    nodes[taskid].name = name;
                } else {
                    nodes[taskid] = {};
                    nodes[taskid].name = name;
                }
                
            }

            nodes[tid].repop = repopulateVals;
            nodes[tid].output = outputName;
                
            localStorage.nodes = JSON.stringify(nodes);

            $("#workflow").empty();

            $("#workflow").nodelink({
                data: data,
                nodeCharge: tangelo.accessor({value: -10000}),
                linkSource: tangelo.accessor({field: "source"}),
                linkTarget: tangelo.accessor({field: "target"}),
                nodeColor: tangelo.accessor({field: "type"}),
                nodeLabel: tangelo.accessor({field: "name"}),
                nodeUID: tangelo.accessor({field: "uid"}),
            });

            var re = new RegExp("^.+[.](png|nc)$");
            if (re.test(results.result)) {
                var download = confirm("Workflow Resulted In:\n" + results.result + ".\n Would you like to download?");

                if (download) {
                    window.open("python/" + results.result);
                }
            } else {
                alert("Results of Workflow:\n" + results.result);
            }

        } else {
            alert(JSON.stringify(results));
        }
    });
}
