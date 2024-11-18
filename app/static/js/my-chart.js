function drawCateChart(labels , data){
//cateStats là tên id  bên index
 const ctx = document.getElementById('cateStats');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels, //Nhãn
      datasets: [{
        label: '# Số lượng',
        data: data,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
function drawRevenueChart(labels, data) {
const ctx = document.getElementById('revenueStats');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Doanh thu',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'green', 'blue', 'rgba(198, 111, 90, 0.8)', 'rgba(255, 199, 120, 0.8)']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
  }