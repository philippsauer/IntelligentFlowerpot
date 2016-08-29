// Parse local CSV file
function parseData(createGraph) {
	Papa.parse("../data.csv", {
		download: true,
		complete: function(results) {
			createGraph(results.data);
		}
	});
}

function createGraph(data) {
	var date = [];
	var temp = [];
	var humidity = [];
	var brigthness = [];
	var level = [];
	
	for (var i = 0; i < data.length; i++) {
		date.push(data[i][0]);
		temp.push(data[i][1]);
		humidity.push(data[i][2]);
		brigthness.push(data[i][3]);
		level.push(data[i][4]);
	}
	
	console.log(date);
	console.log(temp);
	console.log(humidity);
	console.log(brigthness);
	console.log(level);
	
	var ctx_temp = document.getElementById("beleuchtungsChart");
	var tempChart = new Chart(ctx_temp, {
      type: 'line',
      data: {
				
          labels: date,
          datasets: [{
						label: "Temperatur",
            fill: false,
						lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: temp
          }]
					
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
      }
  });
	var ctx_multiple = document.getElementById("multipleChart").getContext("2d");
	ctx_multiple.canvas.width = 600;
	ctx_multiple.canvas.height = 600;
	var multiplelChart = new Chart(ctx_multiple, {
      type: 'line',
      data: {
				
          labels: date,
          datasets: [
						{
							label: "Temperatur",
							fill: false,
							lineTension: 0.1,
							backgroundColor: "rgba(255,0,0,0.4)",
							borderColor: "rgba(255,0,0,1)",
							borderCapStyle: 'butt',
							borderDash: [],
							borderDashOffset: 0.0,
							borderJoinStyle: 'miter',
							pointBorderColor: "rgba(255,0,0,1)",
							pointBackgroundColor: "#fff",
							pointBorderWidth: 1,
							pointHoverRadius: 5,
							pointHoverBackgroundColor: "rgba(255,0,0,1)",
							pointHoverBorderColor: "rgba(220,220,220,1)",
							pointHoverBorderWidth: 2,
							pointRadius: 1,
							pointHitRadius: 10,
							data: temp
						},
						{
							label: "Luftfeuchtigkeit",
							fill: false,
							backgroundColor: "rgba(74,215,0,0.4)",
							borderColor: "rgba(74,215,0,1)",
							borderCapStyle: 'butt',
							borderDash: [],
							borderDashOffset: 0.0,
							borderJoinStyle: 'miter',
							pointBorderColor: "rgba(74,215,0,1)",
							pointBackgroundColor: "#fff",
							pointBorderWidth: 1,
							pointHoverRadius: 5,
							pointHoverBackgroundColor: "rgba(74,215,0,1)",
							pointHoverBorderColor: "rgba(220,220,220,1)",
							pointHoverBorderWidth: 2,
							pointRadius: 1,
							pointHitRadius: 10,
							data: humidity
						},
						{	
							label: "Helligkeit",
							fill: false,
							backgroundColor: "rgba(255,255,0,0.4)",
							borderColor: "rgba(255,255,0,1)",
							borderCapStyle: 'butt',
							borderDash: [],
							borderDashOffset: 0.0,
							borderJoinStyle: 'miter',
							pointBorderColor: "rgba(255,255,0,1)",
							pointBackgroundColor: "#fff",
							pointBorderWidth: 1,
							pointHoverRadius: 5,
							pointHoverBackgroundColor: "rgba(255,255,0,1)",
							pointHoverBorderColor: "rgba(220,220,220,1)",
							pointHoverBorderWidth: 2,
							pointRadius: 1,
							pointHitRadius: 10,
							data: brigthness		
						},
						{
							label: "Füllstand Regentonne",
							fill: false,
							lineTension: 0.1,
							backgroundColor: "rgba(75,192,192,0.4)",
							borderColor: "rgba(75,192,192,1)",
							borderCapStyle: 'butt',
							borderDash: [],
							borderDashOffset: 0.0,
							borderJoinStyle: 'miter',
							pointBorderColor: "rgba(75,192,192,1)",
							pointBackgroundColor: "#fff",
							pointBorderWidth: 1,
							pointHoverRadius: 5,
							pointHoverBackgroundColor: "rgba(75,192,192,1)",
							pointHoverBorderColor: "rgba(220,220,220,1)",
							pointHoverBorderWidth: 2,
							pointRadius: 1,
							pointHitRadius: 10,
							data: level				
						}
					]
					
      },
      options: {
				maintainAspectRatio: true,
				responsive: true,
				title:{
						display:true,
						text:'Intelligenter Blumentopf'
				},
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero:true
						}
					}]
				}
      }
  });
}

parseData(createGraph);


/*$( document ).ready(function() {
	
  var ctx = document.getElementById("beleuchtungsChart");
  var tempChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: ["28.06.2016", "29.06.2016", "30.06.2016", "01.07.2016", "02.07.2016", "03.07.2016"],
          datasets: [{
              data: [12, 19, 3, 5, 2, 3]
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
      }
  });
});*/