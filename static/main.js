$( document ).ready(function() {


  var ctx = document.getElementById("beleuchtungsChart");
  var myChart = new Chart(ctx, {
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
});