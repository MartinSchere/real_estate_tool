$(document).ready(function () {
  let data;

  $.ajax({
    method: "GET",
    url: "/api/chart-data",
    async: false,
  }).done(function (res) {
    data = res;
  });

  console.log(data);
  var ctx1 = $("#incomeChart");
  var incomeChart = new Chart(ctx1, {
    type: "doughnut",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Sources",
          data: data.data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(54, 162, 235, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(54, 162, 235, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      legend: { position: "bottom" },
    },
  });
});
