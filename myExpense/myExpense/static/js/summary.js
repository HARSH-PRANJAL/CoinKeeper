const renderChart = (data, labels) => {
  const ctx = document.getElementById("myChart");

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 month expenses",
          data: data,
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 205, 86)",
          ],
          hoverOffset: 4,
        },
      ],
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Expenses per category",
        },
      },
    },
  });
};

const getChartData = async () => {
  try {
    const response = await fetch("/expenseSummary");
    if (!response.ok) {
      throw new Error(`Error fetching data: ${response.statusText}`);
    }
    const data = await response.json();
    console.log("data", data);
    const result = data.expenseSummaryData;
    const [labels, resultData] = [Object.keys(result), Object.values(result)];
    renderChart(resultData, labels);
  } catch (error) {
    console.error("Error fetching data:", error);
    // Handle error gracefully (e.g., display an error message to the user)
  }
};

document.onload = getChartData(); // Add semicolon here
