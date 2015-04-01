window.onload = function () {
    var url= "python/workflowTwo";
    
    $.getJSON(url, function (results) {
        if(results.workflow) {
            var workflow = results.workflow;
        
            var indexMap = {};
            var i = 0;
            workflow.forEach( function(list) {
                var oldIndex = list[1]
                indexMap[oldIndex] = i;
                i++;
            });

            var data = { nodes: [], links: []};
            workflow.forEach( function(list) {
                data.nodes.push({type: list[0], name: list[0]+list[1]});
                list[2].forEach(function(index) {
                    var sourceIndex = list[1];
                    if(indexMap[index])
                    {
                        data.links.push({source: indexMap[sourceIndex], target: indexMap[index]});
                    }
                });
            });

            var width = $("#content").width();
            var height = $("#content").height();

            var targetParents = {};

            data.links.forEach( function(dict) {
                var source = dict.source;
                var target = dict.target;

                if (targetParents[target]) {
                    targetParents[target].push(source);
                }
                else
                {
                    targetParents[target] = [source];
                }

            });

            var numberOfColumns = Object.keys(targetParents).length + 1;
            var columnSize = width/numberOfColumns;
            var x = columnSize/2;

            for (target in targetParents) {
                targetParents[target].forEach( function(index) {
                    data.nodes[index].x = x;
                });
                x += columnSize;
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
                for(i = 0, len=actualColumnSize; i < actualColumnSize; i++)
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