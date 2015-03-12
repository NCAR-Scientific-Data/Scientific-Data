window.onload = function () {
    var bobbiesReturn = {
        returned: [
            ["subset", [1, 2, 3]],
            ["aggregate", []],
            ["unit conversion", [4]],
            ["unit conversion", [5]],
            ["aggregate", [5]],
            ["range", [6]],
            ["plot", []]
        ]
    }

    var data = { nodes: [], links: []};
    var i = 0;
    bobbiesReturn.returned.forEach( function(list) {
        data.nodes.push({type: list[0], name: list[0]+i});
        list[1].forEach(function(index) {
            data.links.push({source: i, target: index});
        });
        i++;
    });

    var x= 100;

    data.nodes[0].x = x;
    data.nodes[0].y = 300;
    data.nodes[0].fixed = true;

    x += 100

    bobbiesReturn.returned.forEach( function(list) {
        list[1].forEach(function(index) {
            data.nodes[index].x = x;
        });
        x += 100;
    });

    // var data = {
    //     nodes: [
    //         {value: 60, group: 'a', name: 'subset', x: 0, y: 0, fixed: true},
    //         {value: 60, group: 'b', name: 'aggregate'},
    //         {value: 60, group: 'b', name: 'unit conversion'},
    //         {value: 60, group: 'b', name: 'unit conversion'},
    //         {value: 60, group: 'b', name: 'aggregate'},
    //         {value: 60, group: 'b', name: 'range'},
    //         {value: 60, group: 'c', name: 'plot'}
    //     ],
    //     links: [
    //         {s: 0, t: 1},
    //         {s: 0, t: 2},
    //         {s: 0, t: 3},
    //         {s: 2, t: 4},
    //         {s: 4, t: 5},
    //         {s: 3, t: 5},
    //         {s: 5, t: 6},
    //     ]
    // };

    $("#content").nodelink({
        data: data,
        nodeCharge: tangelo.accessor({value: -5000}),
        linkSource: tangelo.accessor({field: "source"}),
        linkTarget: tangelo.accessor({field: "target"}),
        //nodeSize: tangelo.accessor({field: "value"}),
        nodeColor: tangelo.accessor({field: "type"}),
        nodeLabel: tangelo.accessor({field: "name"}),
    });
};
