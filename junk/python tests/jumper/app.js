function Task(name) {
	this.name = name;
	this.next = [];
	this.prev = [];

	this.draw = function(column, numColumns, numInColumn, numInPrevColumn, row){
		var c = document.getElementById("gameCanvas");
		var w = c.width;
		var h = c.height/2;
		var xstride = w/numColumns;
		var ycut = h/numInPrevColumn;
		var ystride = ycut/numInColumn;
		var ctx = c.getContext("2d");
		ctx.fillStyle = "#FF0000";
		// CHANGE
		if(true){
			   ctx.beginPath();
			   ctx.moveTo(xstride*(column-1),h);
    		   ctx.lineTo(xstride*column,h);
    		   ctx.closePath();
    		   ctx.stroke();
		}
		ctx.fillRect(xstride*column, row+ystride*numInColumn, xstride, xstride);
		ctx.fillStyle = "#000000";
		ctx.font="10px Georgia";
		ctx.fillText(name,xstride*column,row+ystride*numInColumn);		
	}
	this.addNext = function(next){
		this.next.push(next);
	}
	this.addPrev = function(prev){
		this.prev.push(prev);
	}
}

var taskLocations = [];
function Workflow(tasks, depth) {
	this.tasks = tasks;
	this.taskLocations = [[]];
	this.numRowsInColumn = [1, 0];



	this.taskLocations = [];

	this.addTasksToLocation = function(task){
		//this.taskLocations.push(task.name);
		if(task.next){
			for(var i = 0; i<task.next.length; i++){
				this.taskLocations.push(task.next[i].name);
			}	
			for(var k = 0; k<task.next.length; k++){
				this.addTasksToLocation(task.next[k]);
			}		
		}



	}

	this.totalLengthChildsChilds = function(task){
		//Calculate number of rows in column 2 steps ahead of current task
		var sum = 0;
		task.next.forEach(function(child){
			sum += child.next.length;
		});
		numRowsInColumn.push(sum);
		numRowsInColumn.push(0);
	}




	this.drawWorkflow = function(task, column, row, prevTaskNum){
		task.draw(column, numColumns, numInColumn, numInPrevColumn, row);
		var l = task.next.length;
		this.totalLengthChildsChilds(task);
		task.prev.next.length;
		for (var i = 0; i < l; i++){
			this.drawWorkflow(task.next[i], column + 2, numRowsInColumn[i-2]*prevTaskNum+(i*row));
		}
		this.tasks[i].draw();
	}
}



function getMaxDepth(task){
		if(task.next.length == 0){
			alert(task.name);
			return 1;
		}	
		else{
			max = 0;
			for (var t in task.next){
				d = getMaxDepth(t)
				if (d > max){
					max = d;					
				}

			}
			return 1 + max;
		}
}

function drawShit(){
	var A = new Task("TaskA");
	var B = new Task("TaskB");
	var C = new Task("TaskC");
	var D = new Task("TaskD");
	A.addNext([B]);
	A.addNext([C]);
	B.addNext([D]);
	B.addPrev([A]);
	C.addNext([D]);
	C.addPrev([A]);
	D.addPrev([C]);
	D.addPrev([B]);
	var w = new Workflow([A, B, C, D]);
	//w.drawWorkflow(A, 1, 7, 1, 1, 1);
	w.addTasksToLocation(A, 0);
	alert(w.taskLocations);
}

drawShit();

