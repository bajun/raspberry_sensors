document.addEventListener('DOMContentLoaded', function() {
    if ("WebSocket" in window) {

        var ws = new WebSocket("ws://" + window.location.host + "/ws");

        ws.onopen = function() {
            console.log("Connected!");
        };

        ws.onmessage = function(evt) {
            var received_msg = JSON.parse(evt.data);


            lineChartDataCo2.datasets[0].data.push(received_msg['co2']);
            lineChartDataHumidity.datasets[0].data.push(received_msg['humidity']);
            var time = new Date(received_msg['time']*1000).toLocaleString();
		// We using common labels, so pushing one time
            lineChartDataCo2.labels.push(time)

            window.chart_с02.update();
            window.chart_humidity.update();

        };


        ws.onclose = function() {
            console.log("Connection is closed")
        };
        ws.onerror = function(event) {
            console.log(event);
        }
        console.log(ws);
    } else {
        console.log("WebSocket NOT supported by your Browser!");
    }
});
