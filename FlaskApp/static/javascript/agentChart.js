google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawLineColors);



function drawLineColors() {


    $.ajax({

        url: "/static/Data/q_learning.json",
        dataType: "json",
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


                    
                    for (var i in biggest)
                        result.push([i, json_data[i], json_data1[i]]);

                    var data = new google.visualization.DataTable();
                    data.addColumn('string', 'X');
                    data.addColumn('number', 'Q-Learning');
                    data.addColumn('number', 'SARSA');

                    data.addRows(result);

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
                        colors: ['#a52714', '#097138'],
                        chartArea: {
                            width: '75%',
                            height: '50%'
                        },
                        width: '95%',

                    };
                    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

                    chart.draw(data, options);
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
