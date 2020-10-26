$(document).ready(function () {
  let data;
  $.ajax({
    method: "GET",
    url: "/api/chart-data/total-expense-chart",
    async: false,
  }).done(function (res) {
    data = res;
  });
  var ctx1 = $("#expenseChart");
  var expenseChart = new Chart(ctx1, {
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
            "rgba(162, 162, 235, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(162, 162, 235, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: { display: true, text: "General", fontFamily: "Helvetica" },
      responsive: true,
      legend: { position: "bottom" },
    },
  });
  let data2;
  $.ajax({
    method: "GET",
    url: "/api/chart-data/property-expenses-chart",
    async: false,
  }).done(function (res) {
    data2 = res;
  });
  var ctx2 = $("#propertyExpensesChart");
  var propertyExpensesChart = new Chart(ctx2, {
    type: "doughnut",
    data: {
      labels: data2.labels,
      datasets: [
        {
          label: "Sources",
          data: data2.data,
          backgroundColor: [
            "rgba(30, 240, 0, 0.2)",
            "rgba(200, 0, 0, 0.2)",
            "rgba(0, 30, 235, 0.2)",
            "rgba(162, 162, 235, 0.2)",
            "rgba(162, 162, 235, 0.2)",
            "rgba(162, 162, 235, 0.2)",
            "rgba(162, 162, 235, 0.2)",
          ],
          borderColor: [
            "rgba(30, 240, 0, 0.2)",
            "rgba(200, 0, 0, 0.2)",
            "rgba(0, 30, 235, 0.2)",
            "rgba(162, 162, 235, 0.2)",
            "rgba(162, 162, 235, 0.2)",
            "rgba(162, 162, 235, 0.2)",
            "rgba(162, 162, 235, 0.2)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: { display: true, text: "Properties", fontFamily: "Helvetica" },
      responsive: true,
      legend: { position: "bottom" },
    },
  });
});
