function alertFunc() {
    $.ajax({
        url: "/static/test.txt",
        dataType: "text",
        success: function (data) {
         var arr =   data.split(/,/g).slice(0);

         for(i=0; i<arr.length-1; i+=2){
             x = arr[i];
             y = arr[i+1];
             $("body").append("third: " + x + "  "+y);
         }



            console.log(arr);
            $("#div1").text(data);
        }
    });
}



function updateFunc() {
    // Box width
    var bw = 400;
    // Box height
    var bh = 400;
    col = 5;
    row = 4;
    gridX = bw/row;
    gridY = bh/col;
    // Padding
    var p = 10;

    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");
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

        url: "/static/test.txt",
        dataType: "text",
        success: function (data) {
            var arr =   data.split(/,/g).slice(0);
            setTimeout(function () {
            for(let i=0; i<arr.length -2; i+=2){
                    x1 = arr[i];
                    y1 = arr[i+1];
                    context.clearRect(0, 0, 500, 500);
                    drawBoard();

                    drawShape(2,  0, 'green');
                    drawShape(2, 1, 'red');
                    drawShape(x1, y1,'yellow');
                    $("body").append("third: " + x1 + "  "+y1);


            }

            }, 10000);
            console.log(arr);
            $("#div1").text(data);
        }
    });


}