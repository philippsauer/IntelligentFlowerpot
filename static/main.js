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
	
	var ctx = document.getElementById("beleuchtungsChart");
	var tempChart = new Chart(ctx, {
      type: 'line',
      data: {
				
          labels: date,
          datasets: [{
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