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

function drawBoard(){

    for (var x = 0; x <= bw; x += gridX) {
        context.moveTo(0.5 + x + p, p);
        context.lineTo(0.5 + x + p, bh + p);
    }


    for (var x = 0; x <= bh ; x += gridY) {
        context.moveTo(p, 0.5 + x + p);
        context.lineTo(bw + p, 0.5 + x + p);
    }

    context.strokeStyle = "black";
    context.stroke();
}



function drawShape(x , y,colour){
    context.strokeRect(p + gridX,p,gridX,gridY);
    context.fillStyle = colour;
    context.fillRect(p + gridX * x,p+ gridY * y,gridX,gridY);
}
$.ajax({

    url: "/static/Data/test.txt",
    dataType: "text",
    cache: false,
    async: true,
    success: function (data) {
        var arr =   data.split(/,/g).slice(0);


        for(let i=0; i<arr.length -2; i+=2){
            window.setTimeout(function () {
                x1 = arr[i];
                y1 = arr[i+1];

                context.clearRect(0, 0, 650, 650);

                drawBoard();

                drawShape(5,  0, 'green');
                drawShape(3,  0, 'red');
                drawShape(5, 1, 'red');
                drawShape(1, 1, 'red');

                drawShape(1, 3, 'red');
                drawShape(2, 4, 'red');
                drawShape(4, 4, 'red');
                drawShape(y1, x1,'yellow');

                //  $("body").append("Pos: " + x1 + "  "+y1);
            }, i * 40);

        }


        //console.log($.unique(position));
        // $("#div1").text(data);
    }

});