function drawBasic() {
    $.ajax({
        type: "GET",
        url: "static/Data/alpha.json",
        dataType: "json",
        cache: false,
        async: true,
        success: function (data) {
            var data = data;
           // console.log(data);

            var json_data = data;

            json_data = json_data[Object.keys(data)[0]];
            var result = [];

            for(var i in json_data)
                result.push([i, json_data [i]]);
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'X');
            data.addColumn('number', 'Agent Reward');

            data.addRows(result);

            var options = {
                title: 'Performance',
                hAxis: {
                    textStyle : {
                        fontSize: 10 // or the number you want
                    },
                    title: 'Episode'


                    //ticks: [0, 25] // display labels every 25
                },
                vAxis: {
                    title: 'Reward Value'
                },
                chartArea: {
                    width: '85%',
                    height: '50%'
                },
                width: '85%',

            };
            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

            chart.draw(data, options);

        }
    });


}

google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawBasic);
