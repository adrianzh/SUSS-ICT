function drawChart(chartData)
{
    const ctx = document.getElementById('myChart').getContext('2d');
    var xLabels = chartData.labels;
    var charts = chartData.charts;
    if (charts === undefined){
        let chartStatus = Chart.getChart("myChart");
        if (chartStatus != undefined) {
            chartStatus.destroy();
        }   
    }
    else{
        // convert the time into string for time chart
        for (const [key, values] of Object.entries(charts)) {
            charts[key] = values.map(value => {
                let d = new Date(value + '+8'); // GMT+8
                let year = d.getFullYear();
                let month = ('' + (d.getMonth() + 1)).padStart(2, '0');
                let day = ('' + d.getDate()).padStart(2, '0');
                let hour = ('' + d.getHours()).padStart(2, '0');
                let mins = ('' + d.getMinutes()).padStart(2, '0');
                return (year + '-' + month + '-' + day + ' ' + hour + ':' + mins + ':00');
            })
        }
        var vLabels = [];
        var vData = [];

        for (const [key, values] of Object.entries(charts)) {
            let xy = []
            vLabels.push(key)
            for (let i = 0; i < values.length; i++) {
                xy.push({ 'x': charts[key][i], 'y': xLabels[i] }) 
            }
            vData.push(xy)
        }
        //To destroy the chart before replacing an existing one
        let chartStatus = Chart.getChart("myChart");
        if (chartStatus != undefined) {
            chartStatus.destroy();
        }   
        var myChart = new Chart(ctx, {
            data: {
            datasets: []
            },
            options: {
                responsive: true,
                maintainaspectratio: false,
                scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour',
                    }
                },
                y: {
                    type: 'category',
                    labels: xLabels,
                    reverse: true,
                    grid: {
                        borderColor: "rgba(249, 238, 236, 0.74)"
                    }
                }
            }
            }
        });
        for (i= 0; i < vLabels.length; i++ ) {
            myChart.data.datasets.push({
            label: vLabels[i], 
            type: "line",
            borderColor: '#'+(0x1100000+Math.random()*0xffffff).toString(16).substr(1,6),
            backgroundColor: "rgba(249, 238, 236, 0.74)",
            data: vData[i],
            spanGaps: true
            });
            myChart.update();
        }
    }
}

//ajax for selection of course
jQuery(document).ready(function($) {
    $("#courseList").on('change', function() {
        var course = $(this).val();

        //ECA
        var getUser = document.getElementById('getUser');
        var filterUser = document.getElementById('filterUser');

        if(course){
            $.ajax({
                url:"/dashboard",
                method:"POST",

                //TMA
                //data:{courseSelect: course},
                //ECA
                data:{courseSelect: course, userByBooking: getUser.value, filterUser: filterUser.value},

                error: function() {
                    alert("Error");
                },
                success: function(data, status, xhr) {
                    drawChart(data)
                }
            }) 
        }
    });
})
//end of ajax
