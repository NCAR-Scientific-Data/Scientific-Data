/*global window, $, tangelo, confirm, alert*/


/*
    Function: getIndexMap
    Maps workflow indices to NodeLink indices.

    Parameters:

        workflow - The workflow JSON object.

    Returns:

        A JavaScript object mapping workflow indices to NodeLink indices.
        The map is formatted "{ originalIndex : nodelinkIndex }"

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
    Generates nodes and links between nodes for visualization.

    Parameters:

        workflow - The workflow JSON object.
        indexMap - A map of workflow indices to NodeLink indices.

    Returns:

        A list with the data javascript object and a breadth-first search
        representation of the workflow.

        _The Data Object_

            *nodes:* A list of nodes. Each node is an object consisting of a 
            node type and a node name.

            *links:* A list of links. Each link is an object with a source node 
            index and a target node index.

        _The Breadth-First Search List_

            The list is such that the index is the parent node, and the children
            of that node are a list stored at that index. For example, say we had
            this tree:

            >       0
            >      / \
            >     1   2
            >    / \
            >   3   4

            Then it would be represented as

            > [
            >   [1,2],
            >   [3, 4],
            >   [ ]
            >   [ ]
            >   [ ]
            > ]

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

        data.nodes[indexMap[nodeIndex]] = {type: nodeType, name: nodeName, uid: nodeUID};

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
    Assigns an initial X value to each node using the breadth-first search list.

    *1.* The web page is divided into columns based on the number of nodes.
    
    *2.* The farthest-left x-value is given to root nodes, and then children nodes are
    assigned an x value equal to the width of the column plus the x value of the
    parent.
    
    *3.* After all x values are assigned, the function returns the number of columns
    it expected to create.

    Parameters:

        data - an object containing lists of the nodes and links.
        bfsList - a list representations of the tree with breadth-first-search

    Returns:

        The number of columns created from the X Values.

    See Also:

        <readjustColumns>

        <generateData>

        <formatWorkflow>
*/
function assignXValue(data, bfsList) {
    "use strict";

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
        for (var j = 0; j < bfsList[i].length; j += 1) {
            data.nodes[bfsList[i][j]].x = tmpx;
        }
    }

    for (var i = 0; i < bfsList.length; i += 1) {
        if (data.nodes[i].x) {
            
        } else {
            data.nodes[i].x = x;
        }
    }

    return numberOfColumns;
}

/*
    Function: readjustColumns
    Modifies node X-values to make columns more even.

    *1.* The function makes a list of all x-values assigned to the nodes.
    
    *2.* The number of actual columns used is the length of the x-values list.
    
    *3.* The old x-values are mapped to the new number of columns.
    
    *4.* Node x-values are adjusted to use the correct x values.

    Parameters:

        data - an object containing lists of the nodes and links.
        numberOfColumns - the number of columns originally created.

    See Also:

        <assignXValue>

        <generateData>

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

    *1.* For each node's children, the children are assigned a y-value, evenly spaced.
    
    *2.* Then the same process is repeated with any missed nodes.

    Parameters:

        data - an object containing all nodes and links.
        bfs - a breadth-first search type representation of the nodes.

    Returns:

        Nothing. Data is modified.

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

        workflow - The workflow list. Each node is a list consisting of the
        node type, the node name, and a list of indices of child nodes.

    Returns:

        The data object fully formatted for nodelink.

    See Also:

        <getIndexMap>

        <generateData>

        <assignXValue>

        <assignYValue>

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
    Add a task to a workflow, run the workflow, and then draw the workflow.

    A Javascript Object of node ids and values for repopulating inputs is saved to localStorage.

    Parameters:

        task_Type - the type of task that is being created.
        links - a Javascript object containing each input for the task.
        repopulateVals - a Javascript object that contains the values for each input on the html page.
        outputName - the name of the output variable in the workflow.

    See Also:

        <formatWorkflow>

        <deleteTask>
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
        if (results.workflow) {
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
        } else {
            alert(JSON.stringify(results));
        }
    });
}

function runWorkflow(){
    "use strict";

    var url = "python/updateWorkflow",
        stuffToPass = {
            "function": "runWorkflow",
            "workflowID": localStorage.uid,
            "args": "None")
        }

    $.getJSON(url, stuffToPass, function (results){
        if (results.result) {
            var re = new RegExp("^.+[.](png|nc)$");
            if (re.test(results.result)) {
                var download = confirm("Workflow Resulted In:\n" + results.result + ".\n Would you like to download?");

                if (download) {
                    window.open("python/" + results.result);
                }
            } else {
                alert("Results of Workflow:\n" + results.result);
            }
        }
    });
}

/*
    Function: deleteTask
    Delete a task from the workflow, run the workflow, and then draw the workflow.

    A Javascript Object of node ids and values for repopulating inputs is saved to localStorage.

    See Also:

        <formatWorkflow>

        <addTask>
*/
function deleteTask() {
    "use strict";

    var url = "python/updateWorkflow",
        stuffToPass = {
            "function" : "deleteTask",
            "workflowID" : localStorage.uid,
            "args" : JSON.stringify([localStorage.current])
        };

    $.getJSON(url, stuffToPass, function (results) {
        if (results.workflow) {
            $("[id^='tangelo-drawer-icon-']").trigger("click");
            $("#analysisWrapper").empty();
            $("#analysisWrapper").html("<h1>NCAR Scientific Workflows</h1>");
            
            var data = formatWorkflow(results.workflow),
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

            delete nodes[localStorage.current];
                
            localStorage.nodes = JSON.stringify(nodes);

            delete localStorage.current;

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

        } else {
            alert(JSON.stringify(results));
        }
    });
}

function updateTask(links, repopulateVals) {
    "use strict";
    var url = "python/updateWorkflow",
        stuffToPass = {
            "function" : "updateTask",
            "workflowID" : localStorage.uid,
            "args" : JSON.stringify([localStorage.current, JSON.stringify(links)])
        };

    var tid = localStorage.current;

    delete localStorage.current;

    $.getJSON(url, stuffToPass, function (results) {
        if (results.workflow) {
            $("[id^='tangelo-drawer-icon-']").trigger("click");
            $("#analysisWrapper").empty();
            $("#analysisWrapper").html("<h1>NCAR Scientific Workflows</h1>");
            
            var data = formatWorkflow(results.workflow),
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

        } else {
            alert(JSON.stringify(results));
        }
    });
}

/*
    Function: saveWorkflow
    Save a workflow to the database, along with its input repopulation values.

    See Also:

        <loadWorkflow>
*/
function saveWorkflow() {
    "use strict";

    var url = "python/updateWorkflow",
        stuffToPass = {
            "function" : "saveWorkflow",
            "workflowID" : localStorage.uid,
            "args" : JSON.stringify([localStorage.nodes])
        };

    $.getJSON(url, stuffToPass, function (results) {
        if (results.result) {
            if (results.result === "true") {
                alert("Your Workflow Has Been Saved. You can access it again by using this serial number:\n" + localStorage.uid);

                var done = confirm("Are you done working?\n Data will be removed from your local computer if you are.\n Don't worry though, your data is backed up.");
                
                if (done) {
                    localStorage.clear();
                    window.location.replace("index.html");
                }
            } else {
                alert("Your workflow could not be saved to the database.\nNo worries, though, your workflow is safe in temporary storage.\nContact <person> for more information.");
            }
        } else {
            alert(JSON.stringify(results));
        }
    });
}
