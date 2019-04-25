/*
*@ Author: Kevin Gleeson
*Version: 1.0
*
*/
//Adapted from: https://developers.google.com/chart/interactive/docs/gallery/linechart
google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawLineColors);

/*

    Google Line Chart for agent performance

 */

function drawLineColors() {

    // Make ajax call
    $.ajax({
        //Request the q learning json file
        url: "/static/Data/q_learning.json",
        dataType: "json",
        // Clear cache for new data after each request
        cache: false,
        async: true,
        success: function (data) {

            var data2 = data;
            // console.log(data);
            $.ajax({

                url: "/static/Data/sarsa.json",
                dataType: "json",
                cache: false,
                async: true,
                success: function (data1) {
                    // To ensure that all of the data is being displayed
                    var data1 = data1;
                    var json_data = data2;
                    var json_data1 = data1;

                    json_data = json_data[Object.keys(data1)[0]];
                    json_data1 = json_data1[Object.keys(data2)[0]];
                    var json_data_size = Object.keys(json_data).length;
                    var json_data1_size = Object.keys(json_data1).length;
                    var result = [];
                    var biggest = [];

                    if(json_data_size>json_data1_size){
                        biggest = json_data;
                    }else if(json_data_size<json_data1_size){
                        biggest = json_data1;
                    }else if(json_data_size==json_data1_size){
                        biggest = json_data1;
                    }


                    // Getting the longest datset
                    for (var i in biggest)
                        result.push([i, json_data[i], json_data1[i]]);
                    // Setup the chart
                    var data = new google.visualization.DataTable();
                    // Adding coulmns
                    data.addColumn('string', 'X');
                    data.addColumn('number', 'Q-Learning');
                    data.addColumn('number', 'SARSA');
                    // Adding the json data
                    data.addRows(result);
                    // Set the options
                    var options = {
                        title: 'Performance',
                        hAxis: {
                            textStyle: {
                                fontSize: 10 // or the number you want
                            },
                            title: 'Episode'


                            //ticks: [0, 25] // display labels every 25
                        },
                        vAxis: {
                            title: 'Reward Value'
                        },
                        // Colours of the chart data
                        colors: ['#a52714', '#097138'],
                        // The size of the chart
                        chartArea: {
                            width: '75%',
                            height: '50%'
                        },
                        width: '95%',

                    };
                    // Create a new chart
                    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
                    // Draw the chart
                    chart.draw(data, options);
                    // For reponsive abillity
                    function resizeHandler () {
                        chart.draw(data, options);
                    }
                    if (window.addEventListener) {
                        window.addEventListener('resize', resizeHandler, false);
                    }
                    else if (window.attachEvent) {
                        window.attachEvent('onresize', resizeHandler);
                    }
                }
            });
        }

    });
}
