var preselect_comments;

function loadComments(data){
    preselect_comments = JSON.parse(data);
    console.log(preselect_comments);

    var dict = {};

    // Retrieving the values
    for (var i = 0; i < preselect_comments.length; i++) {
//        console.log(preselect_comments[i].fields)

        var target_id = preselect_comments[i].fields.target_id;
        var goal_id = preselect_comments[i].fields.goal_id;
        var comment_id = preselect_comments[i].fields.comment_id;

        var relevance_element = $('#relevance_T' + target_id + '_G' + goal_id)[0];
        var relevance = relevance_element.options[relevance_element.selectedIndex].value;
        console.log(relevance)

        if (dict['T' + target_id + '_G' + goal_id]) {
            dict['T' + target_id + '_G' + goal_id].push(comment_id);
        } else {
            dict['T' + target_id + '_G' + goal_id] = [];
            dict['T' + target_id + '_G' + goal_id].push(comment_id);
        }


//      Chaining the select options
        if (relevance == 'positive') {
            $("#comment_T" + target_id + '_G' + goal_id + " .option-positive-header").removeAttr("hidden");
            $("#comment_T" + target_id + '_G' + goal_id + " .option-negative-header").attr('hidden', '');
            $("#comment_T" + target_id + '_G' + goal_id).selectpicker('deselectAll');


        } else if (relevance == 'negative') {
            $("#comment_T" + target_id + '_G' + goal_id + " .option-positive-header").attr('hidden', '');
            $("#comment_T" + target_id + '_G' + goal_id +" .option-negative-header").removeAttr("hidden");
            $("#comment_T" + target_id + '_G' + goal_id).selectpicker('deselectAll');

        } else {
            $("#comment_T" + target_id + '_G' + goal_id + " .option-positive-header").removeAttr("hidden");
            $("#comment_T" + target_id + '_G' + goal_id + " .option-negative-header").removeAttr("hidden");
            $("#comment_T" + target_id + '_G' + goal_id).selectpicker('deselectAll');

        }

    }

    console.log(dict)

    for (var key in dict) {
        $('#comment_' + key).val(dict[key]);
        console.log($('#comment_' + key))
    }

    $('.selectpicker').selectpicker('refresh')

}