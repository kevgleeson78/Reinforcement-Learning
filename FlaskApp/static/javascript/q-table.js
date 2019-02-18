var csvRowCheck=[];

var arrays = [], size = 2;

$.ajax({

    url: "/static/Data/test.txt",
    dataType: "text",
    cache: false,
    async: true,
    success: function (data) {
        var arrt = data.split(/,/g).slice(0);
        var terminal = [[4,2],[4,4],[3,1],[1,1],[1,5],[0,3],[0,5]];

        while (arrt.length > 0) {

            arrays.push(arrt.splice(0, size));
        }

        function multiDimensionalUnique(arr3) {
            var uniques = [];
            var itemsFound = {};
            for(var i = 0, l = arr3.length; i < l; i++) {

                var stringified = JSON.stringify(arr3[i]);
                if(itemsFound[stringified]) { continue; }

                uniques.push(arr3[i]);

                itemsFound[stringified] = true;

            }

            return uniques;
        }
        arrays.pop(0);

        arrays = multiDimensionalUnique(arrays);
        for(var x = 0; x < arrays.length; x++){

            //Iterate through all elements in second array
            for(var y = 0; y < terminal.length; y++){

                /*This causes us to compare all elements
                   in first array to each element in second array
                  Since md1[x] stays fixed while md2[y] iterates through second array.
                   We compare the first two indexes of each array in conditional
                */
                if(arrays[x][0] == terminal[y][0] && arrays[x][1] == terminal[y][1]){
                    arrays.splice(x, 1);
                    //console.log(arrays);
                }
            }
        }
    }
});

// AJAX in the data file

$.ajax({
    type: "GET",
    url: "static/Data/Dataframe.csv",
    dataType: "text",
    cache: false,
    async: true,
    success: function(data) {
        var data =data;
       // console.log(data)
        result = data.split(/\r\n|\n|\r/).reduce((r, s) => {
            var array = s.split(',').map(Number);
            if (!array[0]) {
                r.push([]);
            }
            r[r.length - 1].push(...array);
            return r;
        }, []);

        for(let i=0; i<result.length; i++){

            window.setTimeout(function () {
                for(j=0; j< (result[i].length-1) / 5; j++){
                    csvRowCheck = result[i].slice(j * 5, (j + 1) * 5);
                    if(csvRowCheck[0]==0){
                        $('.data').remove();
                    }

                    $('table').append('<tr class="data"><td>'+csvRowCheck[0] + '</td><td>'+csvRowCheck[1] + '</td><td>'+csvRowCheck[2] + '</td><td>'+csvRowCheck[3] + '</td><td>'+csvRowCheck[4] + '</td><td>'+arrays[j]+ '</td></tr>');

                }

            },i*80);
        }
    }
});