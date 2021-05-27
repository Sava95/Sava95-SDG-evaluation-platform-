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
    var relevance_list = $('#relevance_list')[0].value
    var sdg_country_value_list = $('#sdg_country_value_list')[0].value

    // Chart creation
    var canvas = document.getElementById('relevance_result').getContext('2d');

    var marksData = {
      labels: ["SDG_1", 'SDG_2', "SDG_3", "SDG_4", "SDG_5", "SDG_6", "SDG_7", "SDG_8", "SDG_9", "SDG_10", "SDG_11",
               "SDG_12", "SDG_13", "SDG_14", "SDG_15", "SDG_16", "SDG_17"],
      datasets: [{
        label: "Relevance",
        backgroundColor: backgroundColor_list[5],
        borderColor: borderColor_list[5],
        data: JSON.parse(relevance_list)
      }, {
        label: "Country Values",
        backgroundColor: backgroundColor_list[1],
        borderColor: borderColor_list[1],
        data: JSON.parse(sdg_country_value_list)
      }]
    };

    var radarChart = new Chart(canvas, {
      type: 'radar',
      data: marksData
    });




})