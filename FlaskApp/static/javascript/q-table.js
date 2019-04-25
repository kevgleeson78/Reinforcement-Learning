/*
*@ Author: Kevin Gleeson
*Version: 1.0
*
*/
// Array to check each row in the q table
var csvRowCheck=[];
// Array to hold the agent position in the q table rows
var arrays = [], size = 2;
// Ajax call for the agent position 
$.ajax({

    url: "/static/Data/agentPos.txt",
    dataType: "text",
    cache: false,
    async: true,
    success: function (data) {
		// Array to hold the hard coded terminal states
        var terminal = [[],[]];
		// Terminal states for the cliff grid
        if(grid_type == "grid_cliff") {
            terminal = [[5, 1], [5, 2], [5, 3], [5, 4], [5, 5]];
        }
		// terminal states for the standard grid
        if(grid_type == "grid_standard"){
            terminal = [[3,2],[2,2],[4,4],[3,4],[1,5],[0,5]];
        }
		// slice the data at every ',' into and array 
        var arrt = data.split(/,/g).slice(0);
		
        while (arrt.length > 0) {
			// Splice the array into gropus of single array for every two x, y touples 
            arrays.push(arrt.splice(0, size));
        }
		// Function to get ordered set from the array values.
		// This will allow for the displaying of the position first
		// visited by the agent within the q table.
		// As this will change each time the program is run we need a orderd set of tuples to
		// accuratley get the correct cordinates for each state visited.
		// Adapted from : https://stackoverflow.com/questions/20339466/how-to-remove-duplicates-from-multidimensional-array
        function multiDimensionalUnique(arr3) {
			// Unique array
            var uniques = [];
			// set to hold unique values
            var itemsFound = {};
			// loop through the methods param input.
            for(var i = 0, l = arr3.length; i < l; i++) {
				// convert the data to json
                var stringified = JSON.stringify(arr3[i]);
				// Condition for end of data
                if(itemsFound[stringified]) { continue; }
				// put the arrays into the uniques array
                uniques.push(arr3[i]);
				// For recursive call of items found
                itemsFound[stringified] = true;

            }
			//return the unique ordered list 
            return uniques;
        }
		// The last element of the array is empty pop removes it.
        arrays.pop(0);
		// Get the data from the method multiDimensionalUnique
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

// AJAX call to the csv file Q_Table.csv

$.ajax({
    type: "GET",
    url: "static/Data/Q_Table.csv",
    dataType: "text",
    cache: false,
    async: true,
    success: function(data) {
		// Array of data
        var data =data;
       // console.log(data)
	   // Split csv column data into arrays after every zero index value
	   // Adapted from : https://stackoverflow.com/questions/54293851/javascript-split-rows-from-csv-file-based-on-value-in-first-column/54295247#54295247
        result = data.split(/\r\n|\n|\r/).reduce((r, s) => {
            var array = s.split(',').map(Number);
            if (!array[0]) {
                r.push([]);
            }
            r[r.length - 1].push(...array);
            return r;
        }, []);
		//Populate the Q-Table
        for(let i=0; i<result.length; i++){
			// Timeout for parsing the array of data
            window.setTimeout(function () {
				// Get every 5th column for each row
                for(j=0; j< (result[i].length-1) / 5; j++){
					// Store the 5 columns in array
                    csvRowCheck = result[i].slice(j * 5, (j + 1) * 5);
					// Clear the data after every zero index
					// Allows for updating the data after every frame
                    if(csvRowCheck[0]==0){
                        $('.data').remove();
                    }
					// Add the data to the html table on the reult page
					// Truncating the amount of floating point dcimal places to 7 to save space on the page.
                    $('table').append('<tr class="data"><td>'+csvRowCheck[0] + '</td><td>'+csvRowCheck[1].toFixed(7) + '</td><td>'+csvRowCheck[2].toFixed(7) + '</td><td>'+csvRowCheck[3].toFixed(7) + '</td><td>'+csvRowCheck[4].toFixed(7) + '</td><td>'+arrays[j]+ '</td></tr>');

                }
				// The Hottie framework to heatmap the values in the table as they update
				// Adapted from : https://github.com/DLarsen/jquery-hottie
                $("#q_table td:not(:first-child, :last-child)").hottie({
                    colorArray : [
                        "#F8696B",
                        "#FBE983",
                        "#63BE7B",
                        "#63BE7B",
                        "#63BE7B",
                        "#63BE7B"
                    ]
                });
				// Set the frame rate.
            },i*100);
        }
    }
});
