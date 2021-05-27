var backgroundColor_list = ['rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                          ];

var borderColor_list = ['rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                       ];


$(function() {
    var sdg_code_list = $('#sdg_country_value_list')
    var relevance_list = $('#relevance_list')
    var sdg_country_value_list = $('#sdg_country_value_list')

    // Chart creation
    var marksCanvas = document.getElementById('relevance_result').getContext('2d');



//    var marksCanvas = document.getElementById("marksChart");

    var marksData = {
      labels: ["English", "Maths", "Physics", "Chemistry", "Biology", "History"],
      datasets: [{
        label: "Student A",
        backgroundColor: "rgba(200,0,0,0.2)",
        data: [65, 75, 70, 80, 60, 80]
      }, {
        label: "Student B",
        backgroundColor: "rgba(0,0,200,0.2)",
        data: [54, 65, 60, 70, 70, 75]
      }]
    };

    var radarChart = new Chart(marksCanvas, {
      type: 'radar',
      data: marksData
    });




})