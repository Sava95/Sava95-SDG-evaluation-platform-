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

var target_code = document.getElementById('target_code').value;
var user_ids = document.getElementById('user_ids').value;
var sector_id = document.getElementById('sector_id').value;

$(function() {
    $.ajax({
       type: 'GET',
       url: '/charts/',
       data: {
        target_code: target_code,
        user_ids: JSON.stringify(user_ids),
        sector_id: sector_id,
       },
       success: function(data) {

        var obj = JSON.parse(data);
        console.log(obj);

        var user_ids = obj.user_ids;
        var prof_background_unique = obj.prof_background_unique;
        var prof_background_count = obj.prof_background_count;
        var sector_unique = obj.sector_unique;
        var sector_count = obj.sector_count;
        var positive_comment_unique = obj.positive_comment_unique;
        var positive_comment_count = obj.positive_comment_count;
        var negative_comment_unique = obj.negative_comment_unique;
        var negative_comment_count = obj.negative_comment_count;
        var other_comments = obj.other_comments;
        var loc_spec_true = obj.loc_spec.true_count;
        var loc_spec_false = obj.loc_spec.false_count;

        console.log(loc_spec_true)
        console.log(loc_spec_false)

        // Professional Background Chart
        var ctx_1 = document.getElementById('prof_back').getContext('2d');
        var x_axis = prof_background_unique;
        var y_axis = prof_background_count;

        var prof_back_chart = new Chart(ctx_1, {
            type: 'pie',
            data: {
                labels: x_axis,
                datasets: [{
                    label: '# of Votes',
                    data: y_axis,
                    backgroundColor: backgroundColor_list,
                    borderColor: borderColor_list,
                    borderWidth: 1
                }]
            },
            options: {
                 legend: {
                    display: true,
                    position: 'right',
                 },

            }
        });

        // Sectors Chart
        var ctx_2 = document.getElementById('sector').getContext('2d');
        var x_axis = sector_unique;
        var y_axis = sector_count;

        var prof_back_chart = new Chart(ctx_2, {
            type: 'pie',
            data: {
                labels: x_axis,
                datasets: [{
                    label: '# of Votes',
                    data: y_axis,
                    backgroundColor: backgroundColor_list,
                    borderColor: borderColor_list,
                    borderWidth: 1
                }]
            },
            options: {
                 legend: {
                    display: true,
                    position: 'right',
                 },

            }
        });

        // Location Specific chart
        var ctx_3 = document.getElementById('loc_spec').getContext('2d');
        var x_axis = ['Applicable ', 'Not applicable'];
        var y_axis = [loc_spec_true, loc_spec_false];

        var loc_spec_chart = new Chart(ctx_3, {
            type: 'bar',
            data: {
            labels: x_axis,
            datasets: [{
                data: y_axis,
                backgroundColor: "#3e95cd",
                fill: false
              }
            ]
            },
            options: {
                legend: {
                    display: false,
                 },

                scales: {
                    yAxes: [{
                        ticks: {
                            suggestedMin: 0,
                            suggestedMax: Math.max(...y_axis) + 2,
                        }
                    }]
                },

                title: {
                  display: true,
                  text: 'Location specific chart'
                }
            }
        });

        // Positive Comments Chart
        var ctx_4 = document.getElementById('positive_comments').getContext('2d');
        var unique_comments = positive_comment_unique;
        var comment_count = positive_comment_count;

        var prof_back_chart = new Chart(ctx_4, {
            type: 'horizontalBar',
            data: {
            labels: unique_comments,
            datasets: [{
                data: comment_count,
                backgroundColor: "#3e95cd",
                fill: false
              }
            ]
            },
            options: {
                legend: {
                    display: false,
                 },

                scales: {
                    xAxes: [{
                        ticks: {
                            suggestedMin: 0,
                            suggestedMax: Math.max(...comment_count) + 2,
                        },

                        scaleLabel: {
                            display: true,
                            labelString: 'Number of users'
                        }
                    }]
                },

                title: {
                  display: true,
                  text: 'Positive predefined comments'
                }
            }
        });

        // Negative Comments Chart
        var ctx_5 = document.getElementById('negative_comments').getContext('2d');
        var unique_comments = negative_comment_unique;
        var comment_count = negative_comment_count;

        var prof_back_chart = new Chart(ctx_5, {
            type: 'horizontalBar',
            data: {
            labels: unique_comments,
            datasets: [{
                data: comment_count,
                backgroundColor: "#3e95cd",
                fill: false
              }
            ]
            },
            options: {
                legend: {
                    display: false,
                 },

                scales: {
                    xAxes: [{
                        ticks: {
                            suggestedMin: 0,
                            suggestedMax: Math.max(...comment_count) + 2,
                        },

                        scaleLabel: {
                            display: true,
                            labelString: 'Number of users'
                        }

                    }]
                },

                title: {
                  display: true,
                  text: 'Negative predefined comments'
                }
            }
        });

        // Other Comments
        var tbody = document.getElementById('other_comments_table').getElementsByTagName('tbody')[0];

        for (i = 0; i < other_comments.length; i++){
            // Insert a row at the end of table
            var newRow = tbody.insertRow();

            // Insert a cell at the end of the row
            var newCell_1 = newRow.insertCell();
            newCell_1.style.fontWeight = 'bold';
            newCell_1.setAttribute("class", "col-1");

            var newCell_2 = newRow.insertCell();

            // Append a text node to the cell
            var newText = document.createTextNode(i+1);
            newCell_1.appendChild(newText);

            var newText = document.createTextNode(other_comments[i]);
            newCell_2.appendChild(newText);
        }
       }, // success(data)
    });  // ajax
}); // function({


