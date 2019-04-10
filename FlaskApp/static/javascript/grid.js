//Adapted from : https://stackoverflow.com/questions/11735856/draw-grid-table-on-canvas-html5
// Box width
var bw = 450;
// Box height
var bh = 450;
col = 6;
row = 6;
gridX = bw/row;
gridY = bh/col;
// Padding
var p = 5;

var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");
//context.transform(1, 0, 0, -1, 0, canvas.height)

// For drawing the grid to teh canvas
function drawBoard(){
    // Draw the lines on x axis
    for (var x = 0; x <= bw; x += gridX) {
        context.moveTo(0.5 + x + p, p);
        context.lineTo(0.5 + x + p, bh + p);
    }

    //draw line on y axis
    for (var x = 0; x <= bh ; x += gridY) {
        context.moveTo(p, 0.5 + x + p);
        context.lineTo(bw + p, 0.5 + x + p);
    }
    // colour of the lines
    context.strokeStyle = "black";
    context.stroke();
}


/*
Loading a text file from an ajax call.
Adapted from : https://stackoverflow.com/questions/11589387/load-txt-file-using-jquery-or-ajax
 */

$.ajax({
    //request the agent position text file from the server
    url: "/static/Data/agentPos.txt",
    dataType: "text",
    // Stop caching for new data after each request
    cache: false,
    async: true,
    success: function (data) {
		// Slice each number in the string after each ','
		// data.split puts the values into an array
		// This will allow for the access of each value to be mapped to x, y coordinates
        var arr =   data.split(/,/g).slice(0);
		// Function to draw coloured squares 
		// Red for traps 
		// Green for the goal
		// Yellow for the agent
        function drawShape(x , y,colour){
            context.strokeRect(p + gridX,p,gridX,gridY);
            context.fillStyle = colour;
            context.fillRect(p + gridX * x,p+ gridY * y,gridX,gridY);
        }
		// loop through the x, y coordinate array
		// Two elemetns at a time 
        for(let i=0; i<arr.length -2; i+=2){
			// Time out function for animating the agent
            window.setTimeout(function () {
				// Get the x, y coordinates
                x1 = arr[i];
                y1 = arr[i+1];
				// Clear the canvas after each frame is rendered
                context.clearRect(0, 0, 650, 650);
				// Call teh draw board function
                drawBoard();
				// Check the grid type set by the form input
				// Flask template variable is used to get the value in the result page
                if(grid_type == "grid_standard") {
                    drawShape(5, 0, 'green');
                    drawShape(5, 1, 'red');
                    drawShape(4, 3, 'red');
                    drawShape(4, 4, 'red');
                    drawShape(2, 2, 'red');
                    drawShape(2, 3, 'red');
                    drawShape(y1, x1, 'yellow');
                }
                if(grid_type == "grid_cliff") {
                    drawShape(5, 5, 'green');
                    drawShape(4, 5, 'red');
                    drawShape(3, 5, 'red');
                    drawShape(2, 5, 'red');
                    drawShape(1, 5, 'red');
                    drawShape(y1, x1, 'yellow');
                }
                //  $("body").append("Pos: " + x1 + "  "+y1);
				// Set the frame rate of hte animation
            }, i * 50);

        }


        //console.log($.unique(position));
        // $("#div1").text(data);
    }

});