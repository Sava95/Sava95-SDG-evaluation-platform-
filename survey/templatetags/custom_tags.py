from django.template.defaulttags import register


@register.simple_tag
def get_evaluation(initial_data, goal_id, target_id):
    query = initial_data.get(goal_id)
    relevance = ''
    loc_flag = ''
    note = ''

    if not isinstance(query, list):
        data = query.filter(target_id=target_id).first()

        if data is not None:
            relevance = data.relevance
            loc_flag = data.location_flag
            note = data.note

    return relevance, loc_flag, note


@register.simple_tag
def preselect():
    neutral = str("neutral")
    positive = str("positive")
    negative = str("negative")

    return neutral, positive, negative


@register.simple_tag
def evaluation_check(check, goal_id):

    return check[goal_id-1]     # goal id starts from 1 and check indication from 0


@register.simple_tag
def subtraction_func(number):  # used in comparison.html
    new_number = number - 1

    return new_number


@register.simple_tag
def get_loc_spec(dic, key):
    if dic[key]:   # if dic[key] == True
        return 'Yes'
    else:
        return 'No'


@register.simple_tag
def get_dict_value(dic, key):
    if dic[key]:
        return dic[key]


@register.simple_tag    # used for displaying dropdown menu in front of card element
def zIndex_val(goal_id):
    z_index = 18 - goal_id

    return z_index
