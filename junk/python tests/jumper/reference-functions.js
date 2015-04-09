var SPACE = 40;

// convert grid coordinates to pixel coordinates
function grid(input){
	return input*SPACE;
}
// convert pixel coords to grid coordinates
function inverseGrid(input){
	return input/SPACE;
}


function testFinish(nextlvl){
	console.log("testing finish....");
        for(var m = 0; m < tileArray.length; m++){
            for(var n = 0; n < tileArray[0].length; n++){

                if(tileArray[m][n].value == "untouched"){
                	console.log("FOUND untouched AT ["+m+"]["+n+"]");
                    return;
                }
                console.log("touched.");
            }
        }
    next_lvl(nextlvl);
    console.log("finished");
    return;
}
function next_lvl(nextlvl){  
	var next = "puzzle"+nextlvl+".html" 
	if (nextlvl == "2"){
		window.open(next, "_blank", "height=240, width=240, resizable = no, toolbar = no, scrollbars = no, menubar = no, location = 0, titlebar = no, status = no, top = 180, left = 300");
	}
	else if(nextlvl == "3"){
		window.open(next, "_blank", "height=640, width=160, resizable = no, toolbar = no, scrollbars = no, menubar = no, location = 0, titlebar = no, status = no, top = 60, left = 545");
	}
	else if(nextlvl == "4"){
		window.open(next, "_blank", "height=160, width=520, resizable = no, toolbar = no, scrollbars = no, menubar = no, location = 0, titlebar = no, status = no, top = 60, left = 710");
	}
	else if(nextlvl == "5"){
		window.open(next, "_blank", "height=480, width=440, resizable = no, toolbar = no, scrollbars = no, menubar = no, location = 0, titlebar = no, status = no, top = 180, left = 1235");
	}
	else if(nextlvl == "6"){
        window.open(next, "_blank", "height=500, width=535, resizable = no, toolbar = no, scrollbars = no, menubar = no, location = 0, titlebar = no, status = no, top = 240, left = 705");

}
}
var Player = function(x,y,size,ctx,nextlvl){
	this.x = grid(x);
	this.y = grid(y);
	this.next = nextlvl;
	this.size = SPACE-10;
    this.ctx = ctx;

    this.move = function(deltaX, deltaY){
        

        if ( this.checkCollision(deltaX, deltaY) == false ){
        	// no collision
        	this.x += grid(deltaX);
        	this.y += grid(deltaY);
        	this.ctx.clearRect(0,0,500,500);
        	tileArray[inverseGrid(this.x)][inverseGrid(this.y)].touch();
        	drawGrid(tileArray,this.ctx);
        	this.draw();

        	

        	return;
        }

        else{ // collision detected, do nothing
        	return;}



        this.x = grid(x);
        this.y = grid(y);
        this.draw();
    }
    this.checkCollision = function(deltaX, deltaY){
    	var pX = inverseGrid(this.x);
    	var pY = inverseGrid(this.y);

    	// check tileArray


    	// if attempting to move outside Boundaries in x direction
    	if (pX + deltaX < 0 || pX + deltaX == tileArray.length){
    		console.log("x collision");
    		return true;
    	}
    	// if attempting to move outside Boundaries in y direction
		if (pY + deltaY < 0 || pY + deltaY == tileArray[0].length){
			console.log("y collision");
			return true;
		}

		var nextTileX = pX + deltaX;
		var nextTileY = pY + deltaY;
		var nextTile = tileArray[nextTileX][nextTileY];

		switch (nextTile.value){
			case "untouched":
				return false;
				break;

			case "touched":
				return true;
				break;

			case "wall":
				console.log("wall collision");
				return true;
				break;

			case "finish":
				testFinish(this.next);
				return true;
				break;
		}



    }

    this.draw = function(){
        this.ctx.beginPath();
        this.ctx.rect(	this.x+(SPACE/2)-(this.size/2),
        				this.y+(SPACE/2)-(this.size/2),
        				this.size,
        				this.size);
        
        this.ctx.fillStyle = "rgb(248,248,241)";
        this.ctx.fill();
        this.ctx.closePath();
    }
}

// 
// TILE
// 
var Tile = function(x,y,value,ctx){

	// initial values
	this.x = grid(x);
	this.y = grid(y);
	this.size = SPACE;
	//Value = (start, finish, touched, untouched, wall)
	this.value = value;
	this.touched = false;
	this.ctx = ctx;

	this.drawTile = function (){

		ctx.beginPath();
		var fillColor;
		ctx.rect(this.x,this.y,this.size,this.size);
        ctx.strokeStyle="rgb(248,248,241)";
		switch(this.value){
			case 'start':
				ctx.fillStyle = "rgb(164,227,0)";
				ctx.fill();
				break;
			case 'finish':
				ctx.fillStyle = "rgb(244,42,116)";
				ctx.fill();
				break;
			case 'touched':
				ctx.fillStyle = "rgb(249,153,0)";
				ctx.fill();
				break;
			case 'untouched':
				ctx.fillStyle= "rgb(248,248,241)";
				ctx.fill();
				break;
			case 'wall':
				ctx.fillStyle = "rgb(109,209,229)";
				ctx.fill();
				break;
			case 0:
				ctx.fillStyle = "black";
				break;	
		}
        ctx.stroke();
		ctx.closePath();

	}

	this.touch = function(){
		this.touched = !this.touched;
		if (this.touched){this.value = "touched";}
		else{this.value = "untouched";}
		this.drawTile(ctx);
	}	

} // END TILE


// generate tile array to be drawn
function generateTiles(puzzleArray, ctx){

	var tileArray = [];
	var tileArrayRow = [];
	var value;

	console.log(tileArray.length);

	
	for ( var i=0; i < puzzleArray[0].length; i++){
		
		tileArray.push(tileArrayRow);
		tileArrayRow = [];
		
		for ( var j=0; j < puzzleArray.length; j++){

			// assign value to string
			value = puzzleArray[j][i];

			// if a 0, assign 'untouched'
			if (value == 0){
				value = "untouched";
			}

			tileArray[i][j]= new Tile(i,j,value,ctx);
			tileArray[i][j].drawTile();
		}
	}
	return tileArray;
}

// draw Grid on canvas
function drawGrid(tileArray, canvas){

	for(var i = 0; i < tileArray.length; i++){
		console.log("i");
		for(var j = 0; j < tileArray[0].length; j++){

			tileArray[i][j].drawTile(canvas);

		}

	}
	console.log(tileArray);
}
// });