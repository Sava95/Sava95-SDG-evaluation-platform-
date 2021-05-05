var sector_id_array;

$(document).ready(function() {
//  ################ SURVEY PAGE  ################
    $(".mySubmit").click(function(e){
        e.preventDefault();  // prevents refreshing the page

        var btn_id = $(this).attr('id');   // extended version: button_G1
        var Goal_ID = btn_id.match(/(\d+)/)[0];  // Goal ID: 1, extracting the number from the string,
    //   \d find one or more digits, + - continue after first,

        var targets_list = document.getElementsByName('target_G' + Goal_ID);
        var targets_ID = [];

        for (i = 0; i < targets_list.length; i++){
            targets_ID[i] = targets_list.item(i).value;   // Target IDs: [1, 2, 3, 4, 5]
        };

        var relevance_list = [];
        var loc_flag_list = [];
        var note_list = [];
        var comment_id_list = [];

        for (i = 0; i < targets_list.length; i++){
            let relevance = document.getElementById('relevance_T' + targets_ID[i] + '_G' + Goal_ID);
            let loc_flag = document.getElementById('location_flag_T' + targets_ID[i] + '_G' + Goal_ID);
            let note = document.getElementById('note_T' + targets_ID[i] + '_G' + Goal_ID);
            let comment_ids = $('#comment_T' + targets_ID[i] + '_G' + Goal_ID).val();

            relevance_list[i] = relevance.options[relevance.selectedIndex].value;  // value of selected option
            loc_flag_list[i] = loc_flag.checked;
            note_list[i] = note.value;
            comment_id_list[i] = comment_ids;
        };

        var sector_id = $('.sector_id').val();
        var goal_id = $('.goal_id')[Goal_ID - 1].value;   // $('.goal_id') returns a dictionary that starts from 0, and Goal_ID starts from 1
        var goal_name = $('.goal_name')[Goal_ID - 1].value;

        console.log('Sector ID: ' + sector_id);
        console.log('Goal ID: ' + goal_id);
        console.log('Goal Name: ' + goal_name);

        console.log('target_G' + Goal_ID);
        console.log(targets_ID);
        console.log(relevance_list);
        console.log(loc_flag_list);
        console.log(note_list);
        console.log(comment_id_list);

        // Checking if the user evaluated all targets before saving the SDG
        var evaluation_check = true;

        for (i = 0; i < relevance_list.length; i++){
            if (relevance_list[i] == 'nothing'){
               evaluation_check = false;
            }
        }

        if (evaluation_check == false) {
            $("#error_message_evaluation").show();
            setTimeout(function() { $("#error_message_evaluation").fadeOut("slow"); }, 5000);

        } else {
            $.ajax({
                type: 'POST',
                url: '',
                data: {
                    target_id: targets_ID,
                    sector_id: sector_id,
                    relevance: relevance_list,
                    loc_flag: loc_flag_list,
                    note: note_list,
                    comment_id_list: JSON.stringify(comment_id_list),

                    goal_id: goal_id,
                    goal_name: goal_name,
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken ]').val(),
                },
               success:function(data){
                   console.log(data);  // HTTP Response, from view

                   $("#success_message_evaluation").show();
                   setTimeout(function() { $("#success_message_evaluation").fadeOut("slow"); }, 3000);

                   var img = document.getElementById('img_G' + Goal_ID );
                   if (img != null){
                         img.innerHTML = "<img src='/static/survey/images/check.png' alt='Check Sign' width='36' height='36'>";
                   }

                   var img_sidebar = document.getElementById('img_sidebar_G'+ Goal_ID );
                   if (img_sidebar != null){
                         img_sidebar.innerHTML = "<img src='/static/survey/images/check.png' alt='Check Sign' width='24' height='24'>";
                   }
               }
            })
        }

    }) // mySubmit end

// Bootstrap select-picker: Relevancy select according to
    $('.relevance_select').change(function(){
        var target_id = $(this).attr("id").replace('relevance_','');
        console.log(target_id)

        var comment_id = 'comment_' + target_id;
        console.log(comment_id)

        var relevance = this.options[this.selectedIndex].value;
        console.log(relevance)

        var select_picker_element = document.getElementById(comment_id);
        console.log(select_picker_element)

        if (relevance == 'positive'){
            $("#" + comment_id + " .option-positive-header").removeAttr("hidden");
            $("#" + comment_id + " .option-negative-header").attr('hidden', '');
            $("#" + comment_id).selectpicker('deselectAll')

            $("#" + comment_id).selectpicker('refresh');

        } else if (relevance == 'negative'){
            $("#" + comment_id + " .option-positive-header").attr('hidden', '');
            $("#" + comment_id + " .option-negative-header").removeAttr("hidden");
            $("#" + comment_id).selectpicker('deselectAll')

            $("#" + comment_id).selectpicker('refresh');
        } else {
            $("#" + comment_id + " .option-positive-header").removeAttr("hidden");
            $("#" + comment_id + " .option-negative-header").removeAttr("hidden");
            $("#" + comment_id).selectpicker('deselectAll')

            $("#" + comment_id).selectpicker('refresh');
        }
    })


//   ################ HOME PAGE  ################
   $("#sub_sector").change(function() {
        if ($(this).val() == "yes") {
            $('#copy_sectorDIV').show();
            $('#copy_sector').attr('required', '');
            $('#copy_sector').attr('data-error', 'This field is required.');
        } else {
            $('#copy_sectorDIV').hide();
            $('#copy_sector').removeAttr('required');
            $('#copy_sector').removeAttr('data-error');
        }});

    $(".myCopy").click(function(e){
        e.preventDefault();

        var selectedSector = document.getElementById("home_sector");
        var selectedSector_ID = selectedSector.options[selectedSector.selectedIndex].value;
        var selectedSector_name = selectedSector.options[selectedSector.selectedIndex].innerHTML;

        var copySector =  document.getElementById("copy_sector");
        var copySector_ID = copySector.options[copySector.selectedIndex].value;

        console.log('Sector ID: ' + selectedSector_ID)
        console.log('Copy Sector ID: ' + copySector_ID )

        $.ajax({
            type: 'POST',
            url: '',
            data: {
                selectedSector_ID: selectedSector_ID,
                copySector_ID: copySector_ID,
                csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken ]').val(),
            },
           success:function(){
               if ( selectedSector_ID == copySector_ID ){
                   $("#error_message_evaluation").show();
                   setTimeout(function() { $("#error_message_evaluation").fadeOut("slow"); }, 3000);
               } else {
                    $("#success_message_copy").show();
                    setTimeout(function() { $("#success_message_copy").fadeOut("slow"); }, 3000);

                    var count = 1; // counts how many times the user clicked the myCopy button, used for determine the row number

                    // ################################# History table #################################

                    // ######### Row number #########
                    var table_rows = document.getElementsByClassName("table_rows").length;
                    var row_number = table_rows + count;

                    // ########## All fields checked ##########
                    var all_fields_checked = document.getElementById('sector_id_' + copySector_ID).getAttribute("value");

                    console.log(all_fields_checked)

                    // ########### Date output string ###########
                    var date = new Date();
                    var month_array = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'];
                    var month = month_array[date.getMonth()];
                    var day = date.getDate();
                    var year = date.getFullYear();
                    var hours = date.getHours();
                    console.log(hours)
                    var am_pm = hours >= 12 ? 'p.m.' : 'a.m.';
                    hours = hours % 12;
                    hours = hours ? hours : 12; // the hour '0' should be '12'
                    var minutes = date.getMinutes();
                    minutes = minutes < 10 ? '0'+minutes : minutes; //  :06 instead of just :6 minutes

                    var date_output = month + ' ' + day + ', ' + year + ', ' + hours + ':' + minutes + ' ' + am_pm
                    console.log(date_output)
                    // ########### Update existing rows if they already exist ###########
                    var existing_rows = document.getElementsByClassName('table_rows');

                    if (count == 1) {
                        sector_id_array = [];

                        for (i = 0; i < existing_rows.length; i++){
                            sector_ids = existing_rows.item(i).children[0].id;
                            sector_id_array.push(sector_ids);
                        };
                    };

                    var AFC = document.getElementsByClassName('img_check_' + selectedSector_ID).item(0);
                    var date_posted = document.getElementById("date_posted_" + selectedSector_ID);


                    // ########## History table - Append new row ##########
                    console.log(sector_id_array)
                    console.log(selectedSector_ID)
                    console.log(sector_id_array.includes(selectedSector_ID))

                    if (sector_id_array.includes(selectedSector_ID)){
                        // ### Update existing row ###
                         if (all_fields_checked == 'True'){
                            AFC.innerHTML = "<img src='/static/survey/images/check.png' alt='Check Sign' width='24' height='24'>";
                         } else {
                            AFC.innerHTML = "<img src='/static/survey/images/X.png' alt='Check Sign' width='24' height='24'>";
                         }
                         date_posted.innerHTML = date_output;

                    } else {
                        // ### Add new row to the table ###
                        var tbodyRef = document.getElementById('home_table').getElementsByTagName('tbody')[0];

                        // Insert a row at the end of table
                        var newRow = tbodyRef.insertRow();
                        newRow.classList.add("table_rows");
                        newRow.setAttribute("id", "sector_id_" + selectedSector_ID)

                        // Insert a cell at the end of the row
                        var newCell_1 = newRow.insertCell();
                        newCell_1.style.fontWeight = 'bold';
                        newCell_1.setAttribute("id", selectedSector_ID)

                        var newCell_2 = newRow.insertCell();
                        var newCell_3 = newRow.insertCell();
                        newCell_3.style.paddingLeft  = "6%";
                        newCell_3.classList.add("img_check_" + selectedSector_ID);

                        var newCell_4 = newRow.insertCell();
                        newCell_4.setAttribute("id", "date_posted_" + selectedSector_ID);

                        // Append a text node to the cell
                        var newText = document.createTextNode(row_number);
                        newCell_1.appendChild(newText);

                        var f = document.createElement("form"); //form
                        f.setAttribute('method',"POST");
                        f.setAttribute('action',"/survey/");

                        var t = document.createElement('input'); //tocken
                        t.setAttribute('name', 'csrfmiddlewaretoken');
                        t.setAttribute('type', 'hidden');

                        var csrf_value = document.getElementById("form_" + copySector_ID)[0].value;;
                        t.setAttribute('value', csrf_value);

                        var i = document.createElement("input"); //input element
                        i.setAttribute('type', "hidden");
                        i.setAttribute('name', "sector_id");
                        i.setAttribute('value', selectedSector_ID );

                        var b = document.createElement('button'); //button
                        var newText = document.createTextNode(selectedSector_name);
                        b.appendChild(newText);
                        b.classList.add('button_link');
                        b.type = 'submit';
                        b.name = 'home_table_link';
                        b.value = 'TableLink';

                        f.appendChild(i);
                        f.appendChild(b);
                        f.appendChild(t);

                        newCell_2.appendChild(f);

                        var newIMG = document.createElement("IMG");

                        if (all_fields_checked == 'True'){
                            newIMG.setAttribute("src", "/static/survey/images/check.png")
                        } else {
                            newIMG.setAttribute("src", "/static/survey/images/X.png")
                        };

                        newIMG.setAttribute("width", "24");
                        newIMG.setAttribute("height", "24");
                        newIMG.setAttribute("alt", "Check Sign");

                        newCell_3.appendChild(newIMG);

                        var newText = document.createTextNode(date_output);
                        newCell_4.appendChild(newText);

                        sector_id_array.push(selectedSector_ID); // appends selected sector to the list
                        console.log('After:' + sector_id_array)
                    };
                };
           }
        })
    count++; // counts the number of times the user clicked on the button
    })

var count = 1; // used for finding the sector id

//  ##################### SECTOR PAGE  #####################
    $("#sector_input_form").on('submit', function(e){

        // ######### Row number #########
        var table_rows = document.getElementsByClassName("table_rows").length;
        var row_number = table_rows + 1;

        // ######### Sector input values #########
        var sector_name = document.getElementById('sector_name').value;
        var sector_code = document.getElementById('sector_code').value;
        var sector_level = document.getElementById('sector_level').value;

        if (sector_name == "" || sector_code == "" || sector_level == "" ) {

         } else {

            $.ajax({
              type: 'POST',
              url: '',
              data: {
                  sector_name: sector_name,
                  sector_code: sector_code,
                  sector_level: sector_level,
                  csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken ]').val(),
              },

              success:function(data){
                  console.log(data['sector_id'])
                  if (data['sector_id']) {
                      var sector_id = data['sector_id']
                      console.log('Sector ID: ' + data['sector_id'])

                      $("#success_message_sector").show();
                      setTimeout(function() { $("#success_message_sector").fadeOut("slow"); }, 3000);

                      // ### Add new row to the table ###
                      var tbodyRef = document.getElementById('sector_table').getElementsByTagName('tbody')[0];

                      // Insert a row at the end of table
                      var newRow = tbodyRef.insertRow();
                      newRow.classList.add("table_rows");
                      newRow.setAttribute('id', "sector_id_" + sector_id );

                      // Insert a cell at the end of the row
                      var newCell_1 = newRow.insertCell();
                      newCell_1.style.fontWeight = 'bold';

                      var newCell_2 = newRow.insertCell();
                      newCell_2.setAttribute("id", "sector_name_" + sector_id);

                      var newCell_3 = newRow.insertCell();
                      newCell_3.style.paddingLeft  = "4.5%";
                      newCell_3.setAttribute("id", "sector_code_" + sector_id);

                      var newCell_4 = newRow.insertCell();
                      newCell_4.style.paddingLeft  = "5%";
                      newCell_4.setAttribute("id", "sector_level_" + sector_id);

                      var newCell_5 = newRow.insertCell();

                      // Append a text node to the cell
                      var newText = document.createTextNode(row_number);
                      newCell_1.appendChild(newText);

                      var newText = document.createTextNode(sector_name);
                      newCell_2.appendChild(newText);

                      var newText = document.createTextNode(sector_code);
                      newCell_3.appendChild(newText);

                      var newText = document.createTextNode(sector_level);
                      newCell_4.appendChild(newText);

                      var form = document.createElement("form");
                      form.setAttribute('method',"post");

                      var csrf_token = document.createElement("input");
                      csrf_token.setAttribute("type","hidden");
                      csrf_token.setAttribute("name","csrfmiddlewaretoken");

                      var csrf_value = document.getElementsByName("csrfmiddlewaretoken")[0].value; //the csrf value is the same for all forms
                      csrf_token.setAttribute("value", csrf_value);

                      var newBtn = document.createElement("button");
                      newBtn.innerHTML = 'X';

                      newBtn.setAttribute("value", sector_id); // the id of the new sector is the latest id + 1
                      newBtn.setAttribute("class", "btn btn-danger deleteSector");
                      newBtn.setAttribute("type", "submit");

                      newBtn.style.paddingLeft  = "1rem";
                      newBtn.style.paddingRight  = "1rem";


                      form.appendChild(csrf_token)
                      form.appendChild(newBtn);
                      newCell_5.appendChild(form);

                      $("#sector_input_form").trigger("reset");  // resets the form to initial state

                  } else {
                        $("#error_message_sector").show();
                        setTimeout(function() { $("#error_message_sector").fadeOut("slow"); }, 3000);

                        $("#sector_input_form").trigger("reset");  // resets the form to initial state
                  }
              }
            });

        }
        e.preventDefault();  // prevents refreshing the page
        count++;
    });

    $(document).on('click', '.deleteSector', function(e){
        e.preventDefault();  // prevents refreshing the page

        var sector_id = $(this).attr('value');
        console.log('Sector_id: ' + sector_id)

        var delete_row = document.getElementById("sector_id_" + sector_id);

        var confirmation = window.confirm('Are you sure you want to delete this sector?'); // confirmation message
        console.log(confirmation)

        if (confirmation == false ) {

        } else {
            $.ajax({
              type: 'POST',
              url: '',
              data: {
                  sector_id: sector_id,
                  csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken ]').val(),
              },

            success:function(){
              delete_row.remove()
            }

            });
        };
    });


//  ##################### COMPARISON PAGE  #####################
//  First button: <
    $("#Btn_left").on('click', function(e){
        e.preventDefault();  // prevents refreshing the page

//      Select option lists:
        var chosen_user_list = document.getElementById("chosen_user_select");
        var available_user_list = document.getElementById("available_user_select");

//      Selected object from the Available Users table:
        var selected_user_obj = available_user_list.options[available_user_list.selectedIndex];

        if (selected_user_obj) {
            var selected_user_name = selected_user_obj.text;
            var selected_user_value = selected_user_obj.value;

//          Adding the selected object to the Chosen list
            var new_option = document.createElement("option");
            new_option.text = selected_user_name;
            new_option.value = selected_user_value;
            chosen_user_list.add(new_option)

//          Deleting the chosen object from the Available list
            available_user_list.remove(available_user_list.selectedIndex)

        }

    });

//  Second button: <<
    $("#Btn_double_left").on('click', function(e){
        e.preventDefault();  // prevents refreshing the page

    //      Select option lists:
        var chosen_user_list = document.getElementById("chosen_user_select");
        var available_user_list = document.getElementById("available_user_select");

//      Adding the selected object to the Chosen list
        var i;
        for (i = 0; i < available_user_list.length; i++) {
            var new_option = document.createElement("option");
            new_option.text = available_user_list.options[i].text;
            new_option.value = available_user_list.options[i].value;
            chosen_user_list.add(new_option)
        };

//      Deleting the chosen object from the Available list
        $("#available_user_select").empty();  // deleting all the options in the select list

    });

//  Third button: >
    $("#Btn_right").on('click', function(e){
        e.preventDefault();  // prevents refreshing the page

//      Select option lists:
        var chosen_user_list = document.getElementById("chosen_user_select");
        var available_user_list = document.getElementById("available_user_select");

//      Selected object from the Available Users table:
        var selected_user_obj = chosen_user_list.options[chosen_user_list.selectedIndex];

        if (selected_user_obj) {
            var selected_user_name = selected_user_obj.text;
            var selected_user_value = selected_user_obj.value;

//          Adding the selected object to the Chosen list
            var new_option = document.createElement("option");
            new_option.text = selected_user_name;
            new_option.value = selected_user_value;
            available_user_list.add(new_option);

//          Deleting the chosen object from the Available list
            chosen_user_list.remove(chosen_user_list.selectedIndex)

        }

    });

//  Forth button: >>
    $("#Btn_double_right").on('click', function(e){
        e.preventDefault();  // prevents refreshing the page

//      Select option lists:
        var chosen_user_list = document.getElementById("chosen_user_select");
        var available_user_list = document.getElementById("available_user_select");

//      Adding the selected object to the Chosen list
        var i;
        for (i = 0; i < chosen_user_list.length; i++) {
                var new_option = document.createElement("option");
                new_option.text = chosen_user_list.options[i].text;
                new_option.value = chosen_user_list.options[i].value;
                available_user_list.add(new_option)
            };

//      Deleting the chosen object from the Available list
        $("#chosen_user_select").empty();  // deleting all the options in the select list

    });

    $("#compare_btn").on('click', function(e){
        e.preventDefault();
        $("#loader").show();

        var sector_id_list = document.getElementById('comparison_sector');
        var selected_sector_id = sector_id_list.options[sector_id_list.selectedIndex].value;

        console.log('Sector ID: ' + selected_sector_id)

        var chosen_user_list = document.getElementById('chosen_user_select').children;
        var chosen_users = {}; //dictionary
        var chosen_users_array = [] //list

        console.log(chosen_user_list)

        for (i = 0; i < chosen_user_list.length; i++ ) {
            chosen_users[chosen_user_list[i].text] = chosen_user_list[i].value;
            chosen_users_array.push(chosen_user_list[i].value);
        };

        console.log(JSON.stringify(chosen_users));
        console.log(JSON.stringify(chosen_users_array));

        $.ajax({
              type: 'POST',
              url: '',
              data: {
                  sector_id: selected_sector_id,
                  users: JSON.stringify(chosen_users),

                  csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken ]').val(),
              },

              success:function(data_received){
                   $("#comparison_results").show();
                   $("#comparison_results").carousel(0);
                   $("#loader").hide();

                   var obj = JSON.parse(data_received);
                   console.log(data_received)
                   var user_sector_eval = obj['user_sector_eval'];
                   var comparison_table = obj['comparison_table'];

                   console.log(user_sector_eval)

//                 Warning - If a user didn't complete the survey
                   var user_no_evaluations = [];

                   for (const [key, value] of Object.entries(user_sector_eval)) {
                     if (value[selected_sector_id] == false){
                        user_no_evaluations.push(key)
                     }

                     if (user_no_evaluations === undefined || user_no_evaluations.length > 0) {
                        $("#warning_message").show();
                        setTimeout(function() { $("#warning_message").fadeOut("slow"); }, 5000);

                        var comparison_sector = document.getElementById('comparison_sector')

                        document.getElementById('user_warning').innerHTML = user_no_evaluations
                        document.getElementById('sector_warning').innerHTML = comparison_sector.options[comparison_sector.selectedIndex].text;
                     }
                   }


//                 Comparison Logic
                   var rel_threshold = document.getElementById('comparison_threshold');
                   var threshold_val = rel_threshold.options[rel_threshold.selectedIndex].value;

                   for (i = 1; i <= Object.keys(comparison_table).length; i++){          // goals
                       for (j = 1; j <= Object.keys(comparison_table[i]).length; j++){   // targets
                            var positive_count = comparison_table[i][i + '.' + j].positive;
                            var neutral_count = comparison_table[i][i + '.' + j].neutral;
                            var negative_count = comparison_table[i][i + '.' + j].negative;

                            var count = [positive_count, neutral_count, negative_count];   // [3, undefined, 2] -> [pos, neu, neg]

                            for (item = 0; item < count.length; item++ ){  // if there isn't a count, put 0 instead of undefined
                                if (! count[item]) {
                                    count[item] = 0
                                }
                            }

                            var count_sum = count.reduce((a, b) => a + b, 0) // function(a, b){ return = a + b }, 0
                            // executes a reducer(custom function) on each element of the array, resulting in single output value,
                            // in this case sum of numbers, ,0 -> add a value to the sum (if there is no sum the func will return 0)
//                            console.log(count_sum)

                            var highest_count = Math.max(...count)  // find the largest value in the array
//                            console.log(highest_count)

                            var count_index = count.indexOf(highest_count);  // find the index of that value
                            var count_frequency = count.filter(numb => numb == highest_count).length; // count if there are more than one value
                            var relevance_obj = document.getElementById('target_' + i + '.' + j)

                            var relevance_element_upper = document.getElementById('upper_' + i + '.' + j);
                            var relevance_element_lower = document.getElementById('lower_' + i + '.' + j);

                            var sector_id_element = document.getElementById('sector_id_T_' +  i + '.' + j);
                            sector_id_element.value= selected_sector_id;

                            var user_id_element = document.getElementById('user_ids_T_' +  i + '.' + j);
                            user_id_element.value = chosen_users_array;

                            // Comparison Logic
                            if (highest_count/count_sum*100 >= threshold_val){
                                if (count_frequency == 1){
                                    if (count_index == 0){
                                        var relevance = "<input type='submit' value='Positive' class='indecisive_link' style='background: none; "
                                                                                                                     + "border: none; "
                                                                                                                     + "cursor: pointer;'>";
                                        relevance_obj.style.backgroundColor = "#b5e7a0";  // green
                                        relevance_element_upper.className += ' positive';

                                    } else if ( count_index == 1) {
                                        var relevance = "<input type='submit' value='Neutral' class='indecisive_link' style='background: none; "
                                                                                                                     + "border: none; "
                                                                                                                     + "cursor: pointer;'>";
                                        relevance_obj.style.backgroundColor = "#FFFFFF";   // white
                                        relevance_element_upper.className += ' neutral';

                                    } else if ( count_index == 2) {
                                        var relevance = "<input type='submit' value='Negative' class='indecisive_link' style='background: none; "
                                                                                                                     + "border: none; "
                                                                                                                     + "cursor: pointer;'>";
                                        relevance_obj.style.backgroundColor = "#e57373";  // red
                                        relevance_element_upper.className += ' negative';

                                    }
                                } else {
                                    var relevance = "<input type='submit' value='Indecisive' class='indecisive_link' style='background: none; "
                                                                                                                          + "border: none; "
                                                                                                                          + "cursor: pointer;'>";
                                    relevance_obj.style.backgroundColor = " #ffee58";  // yellow
                                    relevance_element_upper.className += ' indecisive';
                                }

                            } else {
                                var relevance = "<input type='submit' value='Indecisive' class='indecisive_link' style='background: none; "
                                                                                                                     + "border: none; "
                                                                                                                     + "cursor: pointer;'>";

                                relevance_obj.style.backgroundColor = " #ffee58";  // yellow
                                relevance_element_upper.className += ' indecisive';

                            }

                            relevance_element_upper.innerHTML = relevance;

                            relevance_element_lower.innerHTML = '(positive: ' + count[0] +
                                                                '; neutral: ' + count[1] +
                                                                '; negative: ' + count[2] + ')';

                       }
                   }
              }
        })
    });

// ################################## Registration page ##################################
$('#id_professional_background').change(function(){
    if (this.options[this.selectedIndex].value == 'Other') {
        var referenceNode = $('#div_id_professional_background')[0];
        var parent_div = document.createElement('div');
        parent_div.setAttribute('id', 'prof_back_other_DIV')
        insertAfter(parent_div, referenceNode);

        var newNode_1 = document.createElement('label');
        newNode_1.innerHTML = "Insert your professional background* ";
        newNode_1.setAttribute('for', 'prof_back')
        parent_div.appendChild(newNode_1)

        var newNode_2 = document.createElement('input');
        newNode_2.setAttribute('type', 'text')
        newNode_2.setAttribute('name', 'prof_back')
        newNode_2.setAttribute('class', 'form-control')
        newNode_2.setAttribute('style', 'margin-bottom:10px')
        newNode_2.setAttribute('required', 'required')
        parent_div.appendChild(newNode_2)

    } else {
        if ($('#prof_back_other_DIV')) {
            $('#prof_back_other_DIV').remove();
        }
    }
})

$('#id_Sector').change(function(){
    if (this.options[this.selectedIndex].value == 'Other') {
        var referenceNode = $('#div_id_Sector')[0];
        var parent_div = document.createElement('div');
        parent_div.setAttribute('id', 'sector_other_DIV')

        insertAfter(parent_div, referenceNode);

        var newNode_1 = document.createElement('label');
        newNode_1.innerHTML = "Insert sector* ";
        newNode_1.setAttribute('for', 'sector_other')
        parent_div.appendChild(newNode_1)

        var newNode_2 = document.createElement('input');
        newNode_2.setAttribute('type', 'text')
        newNode_2.setAttribute('name', 'sector_other')
        newNode_2.setAttribute('class', 'form-control')
        newNode_2.setAttribute('style', 'margin-bottom:10px')
        newNode_2.setAttribute('required', 'required')
        parent_div.appendChild(newNode_2)

    } else {
        if ($('#sector_other_DIV')) {
            $('#sector_other_DIV').remove();
        }
    }
})

});

//  ##################### Search Filters  #####################
// Comparison page
function filterFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("available_user_search");
    filter = input.value.toUpperCase();
    div = document.getElementById("available_user_select");
    a = div.getElementsByTagName("option");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          a[i].style.display = "";
        } else {
          a[i].style.display = "none";
        }
    }
};

// Sector page
function filterSector() {
    var input, filter, table, tr, td_name, td_code, i, txtValue_name, txtValue_code;
    input = document.getElementById("sector_search");
    filter = input.value.toUpperCase();

    table = document.getElementById("sector_table");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
      td_name = tr[i].getElementsByTagName("td")[0];
      td_code = tr[i].getElementsByTagName("td")[1];

      if (td_name) {
        txtValue_name = td_name.textContent || td_name.innerText;
        txtValue_code = td_code.textContent || td_code.innerText;

        if (txtValue_name.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else if (txtValue_code.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
};

// Home page
function filterHome() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("home_search");
  filter = input.value.toUpperCase();

  table = document.getElementById("home_table");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

// Registration page
function insertAfter(newElement,targetElement) {
    // target is what you want it to go after. Look for this elements parent.
    var parent = targetElement.parentNode;

    // if the parents lastchild is the targetElement...
    if (parent.lastChild == targetElement) {
        // add the newElement after the target element.
        parent.appendChild(newElement);
    } else {
        // else the target has siblings, insert the new element between the target and it's next sibling.
        parent.insertBefore(newElement, targetElement.nextSibling);
    }
}



