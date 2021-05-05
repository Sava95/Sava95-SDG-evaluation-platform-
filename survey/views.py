import json
from django.core import serializers

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from survey.models import User, Sector, Target, Goal, Evaluation, EvaluatedGoal, PredefinedComments, TargetComment, UserProfile
from django.http import HttpResponse
from django.http import JsonResponse
from collections import Counter


@login_required(login_url='login')
def home(request):
    sector = Sector.objects.all()

    #################### Dropdown item list for feature: Copy Sectors ####################
    unique_eval_sector_ids = set(EvaluatedGoal.objects.filter(user_name=request.user.username).values_list('sector_id', flat = True))
    # set - returns the unique values, flat = True - return single values
    sector_ids = set(Sector.objects.values_list('id', flat=True))

    copy_sectors = Sector.objects.none()  # creates empty queryset

    for unique_sector_id in unique_eval_sector_ids:
        for item in sector_ids:
            if unique_sector_id == item:
                copy_sectors |= (Sector.objects.filter(id=unique_sector_id))  # |= appends objects to queryset

    #################### History table ###############
    # History table - Sector Name
    evaluated_sector_ids = set(EvaluatedGoal.objects.filter(user_name=request.user.username).values_list('sector_id', flat = True))
    sorted_eval_sector_ids = sorted(evaluated_sector_ids)

    evaluated_sectors = Sector.objects.filter(id__in=sorted_eval_sector_ids)  # id__in - pass in multiple ids

    # History table - All fields checked
    number_of_goals = len(Goal.objects.all())   # 17
    all_fields_checked = {}
    index = 0

    for sector_id in sorted_eval_sector_ids:
        if EvaluatedGoal.objects.filter(user_name=request.user.username, sector_id = sector_id).count() == number_of_goals:
            all_fields_checked[index] = True
        else:
            all_fields_checked[index] = False

        index = index + 1

    # History table - Most recent date
    evaluated_dates = {}

    for index, sector_id in enumerate(sorted_eval_sector_ids):
        if EvaluatedGoal.objects.filter(user_name=request.user.username, sector_id = sector_id).count() > 1:
            eval_date = EvaluatedGoal.objects.filter(user_name=request.user.username, sector_id = sector_id).order_by('date_posted').reverse()[0]
            evaluated_dates[index] = eval_date.date_posted
        else:
            eval_date = EvaluatedGoal.objects.filter(user_name=request.user.username, sector_id = sector_id).first()
            evaluated_dates[index] = eval_date.date_posted

    # History table - Merging data into objects
    eval_list = []  # list of dictionaries

    for index in range(len(evaluated_sectors)):
        eval_dict = {
            "id": evaluated_sectors[index].id,
            "sector_name": evaluated_sectors[index].sector_code + ' | ' + evaluated_sectors[index].sector_name,
            "all_fields_checked": all_fields_checked[index],
            "date_posted": evaluated_dates[index]
        }
        eval_list.append(eval_dict)

    content = {
        'sectors': sector,
        'copy_sectors': copy_sectors,
        'eval_list': eval_list,
    }

    selectedSector_ID = request.POST.get('selectedSector_ID')
    copySector_ID = request.POST.get('copySector_ID')

    if request.method == 'POST':
        if request.is_ajax():
            # If object doesnt exist in the database
            if not EvaluatedGoal.objects.filter(user_name=request.user.username, sector_id=request.POST.get('selectedSector_ID')).exists():
                # Evaluated goals
                evaluated_goals = EvaluatedGoal.objects.filter(user_name=request.user.username, sector_id=request.POST.get('copySector_ID'))

                for goal in evaluated_goals:
                    goal.id = None   # deleting the id (primary key) will create a new goal instead of updating the same one
                    goal.sector_id = request.POST.get('selectedSector_ID')
                    goal.save()

                evaluations = Evaluation.objects.filter(user_name=request.user.username, sector_id=request.POST.get('copySector_ID'))

                # Evaluations
                for evaluation in evaluations:
                    evaluation.id = None
                    evaluation.sector_id = request.POST.get('selectedSector_ID')
                    evaluation.save()

                # TargetComment
                target_comment = TargetComment.objects.filter(user_name=request.user.username,
                                                              sector_id=request.POST.get('copySector_ID'))

                for comment in target_comment:
                    target_comment = TargetComment()
                    target_comment.user_id = request.user.id
                    target_comment.user_name = request.user.username
                    target_comment.goal_id = comment.goal_id
                    target_comment.sector_id = request.POST.get('selectedSector_ID')
                    target_comment.target_id = comment.target_id

                    target_comment.comment_id = comment.comment_id

                    target_comment.save()

                return HttpResponse('no')

            # If object exist in the database
            else:
                if selectedSector_ID != copySector_ID:
                    # Evaluated goals
                    evaluated_goals = EvaluatedGoal.objects.filter(user_name=request.user.username, sector_id=request.POST.get('copySector_ID'))
                    selected_goals = EvaluatedGoal.objects.filter(user_name=request.user.username, sector_id=request.POST.get('selectedSector_ID'))

                    selected_goals. delete()

                    for goal in evaluated_goals:
                        goal.id = None
                        goal.sector_id = request.POST.get('selectedSector_ID')
                        goal.save()

                    # Evaluations
                    evaluations = Evaluation.objects.filter(user_name=request.user.username, sector_id=request.POST.get('copySector_ID'))
                    selected_evaluations = Evaluation.objects.filter(user_name=request.user.username, sector_id=request.POST.get('selectedSector_ID'))

                    selected_evaluations.delete()

                    for evaluation in evaluations:
                        evaluation.id = None
                        evaluation.sector_id = request.POST.get('selectedSector_ID')
                        evaluation.save()

                    # TargetComment
                    current_target_comment = TargetComment.objects.filter(user_name=request.user.username,
                                                                          sector_id=request.POST.get('selectedSector_ID'))

                    current_target_comment.delete()

                    target_comment = TargetComment.objects.filter(user_name=request.user.username,
                                                                  sector_id=request.POST.get('copySector_ID'))

                    for comment in target_comment:
                        target_comment = TargetComment()
                        target_comment.user_id = request.user.id
                        target_comment.user_name = request.user.username
                        target_comment.goal_id = comment.goal_id
                        target_comment.sector_id = request.POST.get('selectedSector_ID')
                        target_comment.target_id = comment.target_id

                        target_comment.comment_id = comment.comment_id

                        target_comment.save()

                        
                return HttpResponse()

    return render(request, 'survey/home.html', content)


@login_required(login_url='login')
def survey(request):
    Goals = Goal.objects.all()
    PDC = PredefinedComments.objects.all()
    target_set = {}
    initial_data = {}
    check = {}

    for index, goal in enumerate(Goals):
        target_set[goal.id] = Target.objects.filter(goal_id = goal.id)   # set of targets that belong to the same goal

        # Used for setting initial values when re-opening the same survey evaluation page
        if EvaluatedGoal.objects.filter(user_name=request.user.username,
                                        sector_id=request.POST.get('sector_id'),
                                        goal_id=goal.id).exists():
            # could also be done with Evaluation, but in this way it is searching for 1 value instead of n+ values

            initial_data[goal.id] = Evaluation.objects.filter(user_name=request.user.username,
                                                              sector_id=request.POST.get('sector_id'),
                                                              goal_id=goal.id)
        else:
            initial_data[goal.id] = []

        # Check Sign - Returns a dictionary of True or False values
        check[index] = EvaluatedGoal.objects.filter(user_name=request.user.username, sector_id=request.POST.get('sector_id'),
                                                    goal_id=goal.id).exists()

    # Loading comments from DB - preselect comments feature
    preselect_comments = TargetComment.objects.filter(user_name=request.user.username, sector_id =request.POST.get('sector_id'))
    preselect_comments = serializers.serialize('json', preselect_comments)

    content = {
        'target_set': target_set,  # dictionary where each key represents a goal
        'goals': Goals,
        'initial_data': initial_data,
        'check': check,
        'predefined_comments': PDC,
        'preselect_comments': preselect_comments,
    }

    if request.method == 'POST':
        if request.POST.get("home_edit_btn") or request.POST.get("home_table_link"):

            # Edit/create evaluation
            sector_id = request.POST.get("sector_id")
            obj = Sector.objects.get(id = sector_id)
            sector_name = obj.sector_name

            content['sector_id'] = sector_id
            content['sector_name'] = sector_name

            return render(request, 'survey/survey.html', content)

        if request.is_ajax():
            comment_id_list = json.loads(request.POST.get('comment_id_list'))

            # If the evaluation exists, update it
            if EvaluatedGoal.objects.filter(user_name = request.user.username, goal_id = request.POST.get('goal_id'),
                                            sector_id = request.POST.get('sector_id')).exists():
                # Filling in the EvaluationGoal table
                evaluation_goal = EvaluatedGoal.objects.filter(user_name = request.user.username,
                                                               goal_id = request.POST.get('goal_id'),
                                                               sector_id = request.POST.get('sector_id')).first()
                evaluation_goal.user_id = request.user.id
                evaluation_goal.user_name = request.user.username
                evaluation_goal.sector_id = request.POST.get('sector_id')
                evaluation_goal.goal_id = request.POST.get('goal_id')
                evaluation_goal.goal_name = request.POST.get('goal_name')
                evaluation_goal.save()

                # Filling in the Evaluation table
                index = 0

                while index < len(request.POST.getlist("target_id[]")):
                    evaluation = Evaluation.objects.filter(user_name = request.user.username,
                                                           target_id = request.POST.getlist('target_id[]')[index],
                                                           sector_id = request.POST.get('sector_id')).first()
                    evaluation.user_id = request.user.id
                    evaluation.user_name = request.user.username
                    evaluation.goal_id = request.POST.get('goal_id')
                    evaluation.target_id = request.POST.getlist('target_id[]')[index]
                    evaluation.sector_id = request.POST.get('sector_id')
                    evaluation.relevance = request.POST.getlist('relevance[]')[index]

                    if request.POST.getlist('loc_flag[]')[index] == 'true':
                        evaluation.location_flag = True
                    else:
                        evaluation.location_flag = False

                    evaluation.note = request.POST.getlist('note[]')[index]

                    evaluation.save()

                    # Filling in the TargetComment table
                    index_2 = 0

                    target_comment = TargetComment.objects.filter(user_name=request.user.username,
                                                                  goal_id=request.POST.get('goal_id'),
                                                                  target_id=request.POST.getlist('target_id[]')[index],
                                                                  sector_id=request.POST.get('sector_id'))
                    target_comment.delete()

                    if len(comment_id_list[index]) != 0:  # checking if the array is empty
                        while index_2 < len(comment_id_list[index]):
                            target_comment = TargetComment()
                            target_comment.user_id = request.user.id
                            target_comment.user_name = request.user.username
                            target_comment.goal_id = request.POST.get('goal_id')
                            target_comment.sector_id = request.POST.get('sector_id')
                            target_comment.target_id = request.POST.getlist('target_id[]')[index]

                            target_comment.comment_id = comment_id_list[index][index_2]

                            target_comment.save()

                            index_2 = index_2 + 1

                    index = index + 1

            # If the evaluation doesn't exist, make a new one
            else:
                # Filling in the EvaluationGoal table
                evaluation_goal = EvaluatedGoal()
                evaluation_goal.user_id = request.user.id
                evaluation_goal.user_name = request.user.username
                evaluation_goal.sector_id = request.POST.get("sector_id")
                evaluation_goal.goal_id = request.POST.get('goal_id')
                evaluation_goal.goal_name = request.POST.get('goal_name')
                evaluation_goal.save()

                # Filling in the Evaluation table
                index = 0

                while index < len(request.POST.getlist("target_id[]")):
                    evaluation = Evaluation()
                    evaluation.user_id = request.user.id
                    evaluation.user_name = request.user.username
                    evaluation.goal_id = request.POST.get('goal_id')
                    evaluation.target_id = request.POST.getlist('target_id[]')[index]
                    evaluation.sector_id = request.POST.get('sector_id')
                    evaluation.relevance = request.POST.getlist('relevance[]')[index]

                    if request.POST.getlist('loc_flag[]')[index] == 'true':
                        evaluation.location_flag = True
                    else:
                        evaluation.location_flag = False

                    evaluation.note = request.POST.getlist('note[]')[index]

                    evaluation.save()

                    # Filling in the TargetComment table
                    index_2 = 0

                    if len(comment_id_list[index]) != 0:  # checking if the array is empty
                        while index_2 < len(comment_id_list[index]):
                            target_comment = TargetComment()
                            target_comment.user_id = request.user.id
                            target_comment.user_name = request.user.username
                            target_comment.goal_id = request.POST.get('goal_id')
                            target_comment.sector_id = request.POST.get('sector_id')
                            target_comment.target_id = request.POST.getlist('target_id[]')[index]

                            target_comment.comment_id = comment_id_list[index][index_2]

                            target_comment.save()

                            index_2 = index_2 + 1

                    index = index + 1

            return HttpResponse('Ajax was succesfull')

    return render(request, 'survey/survey.html', content)


@login_required(login_url='login')
@staff_member_required
def sectors(request):
    sector_list = Sector.objects.all()

    if Sector.objects.all():  # if there are any objects in the query set
        latest_sector_id = Sector.objects.latest('id').id  # get the id of the last object in the Sectors Query Set, used in JS
    else:
        latest_sector_id = []

    content = {
        'sector_list': sector_list,
        'latest_sector_id': latest_sector_id,
    }

    if request.method == 'POST':
        if request.is_ajax():
            if request.POST.get('sector_name'):  # distinguishing between the ajax calls (save -  has variable sector_name)
                if len(request.POST.get('sector_name')) > 100 or len(request.POST.get('sector_code')) > 20 or len(request.POST.get('sector_level')) > 10:

                    return JsonResponse({'sector_id': None}, safe=False)

                else:

                    sector = Sector()
                    sector.sector_name = request.POST.get('sector_name')
                    sector.sector_code = request.POST.get('sector_code')
                    sector.sector_level = request.POST.get('sector_level')
                    sector.save()

                    sector_id = sector.id

                    return JsonResponse({'sector_id': sector_id}, safe=False)

            else:
                sector_id = request.POST.get('sector_id')
                Sector.objects.filter(id = sector_id).delete()

                return HttpResponse(" Delete button ")

    return render(request, 'survey/sectors.html', content)


@login_required(login_url='login')
@staff_member_required
def comparison(request):
    Sectors = Sector.objects.all()
    Goals = Goal.objects.all()
    target_set = {}

    for index, goal in enumerate(Goals):
        target_set[goal.id] = Target.objects.filter(goal_id = goal.id)   # set of targets that belong to the same goal

    user_ids = set(EvaluatedGoal.objects.all().values_list('user_id', flat = True))  # set of unique user ids
    users = User.objects.filter(id__in = user_ids)

    content = {
        'sectors': Sectors,
        'users': users,
        'goals': Goals,
        'target_set': target_set,  # dictionary where each key represents a goal
    }

    # Checking if all the users evaluated all goals within a sector
    number_of_goals = len(Goal.objects.all())  # 17
    all_fields_checked = {}
    user_sector_eval = {}

    for user in users:
        for sector_id in Sector.objects.all():
            if EvaluatedGoal.objects.filter(user_name=user.username, sector_id=sector_id.id).count() == number_of_goals:
                all_fields_checked[sector_id.id] = True
            else:
                all_fields_checked[sector_id.id] = False

        user_sector_eval[user.username] = all_fields_checked
        all_fields_checked = {}

    content['user_sector_eval'] = user_sector_eval

    if request.method == 'POST':
        if request.is_ajax():
            Goals = Goal.objects.all()

            sector_id = request.POST.get('sector_id')
            users = json.loads(request.POST.get('users'))

            User_evaluations = {}
            Goal_evaluations = {}
            Target_relevance = {}

            # Creating the relevance table that will be used for comparison
            for user, user_id in users.items():   # key: user name, value: user id
                User_evaluations[user] = Goal_evaluations

                for goal in Goals:
                    for target in Target.objects.filter(goal_id = goal.id):

                        relevance_obj = Evaluation.objects.filter(user_id = user_id,
                                                                  sector_id = sector_id,
                                                                  goal_id = goal.id,
                                                                  target_id = target.id).first()

                        if relevance_obj:  # if the user didn't evaluate the target, it takes a default value
                            relevance = relevance_obj.relevance
                        else:
                            relevance = 'neutral'

                        Target_relevance[target.target_code] = relevance

                    Goal_evaluations[goal.id] = Target_relevance

                    Target_relevance = {}
                Goal_evaluations = {}

            # Comparison Logic
            comparison_table = {}
            comparison_targets = {}
            comparison_relevance = {}

            target_eval_list = []

            for goal in Goals:  # goal.id = '1', '2', '3', ...
                for target in Target.objects.filter(goal_id = goal.id):  # target.code = '1.1', '1.2, '1.3', ...
                    for user in users:  # user = 'Sava Nedeljkovic', 'Nikola Catovic', ...
                        relevance = User_evaluations[user][goal.id][target.target_code]  # relevance value: positive, neutral or negative
                        target_eval_list.append(relevance)

                    # Counting the items and the number of times they occurred, in descending order
                    counter = Counter(target_eval_list).most_common()  # define counter and searchable list

                    if len(counter) == 1:  # all users have selected the same relevance for this target
                        high_counter = counter[0]
                        value_high, count_high = high_counter[0], high_counter[1]  # highest occurrence
                        comparison_relevance[value_high] = count_high

                    elif len(counter) == 2:  # the users have selected 2 different relevance for this target
                        high_counter = counter[0]
                        mid_counter = counter[1]

                        value_high, count_high = high_counter[0], high_counter[1]  # highest occurrence
                        value_mid, count_mid = mid_counter[0], mid_counter[1]  # middle occurrence

                        comparison_relevance[value_high] = count_high
                        comparison_relevance[value_mid] = count_mid

                    elif len(counter) == 3:  # the users have selected 3 different relevances for this target
                        high_counter = counter[0]
                        mid_counter = counter[1]
                        low_counter = counter[2]

                        value_high, count_high = high_counter[0], high_counter[1]  # highest occurrence
                        value_mid, count_mid = mid_counter[0], mid_counter[1]  # middle occurrence
                        value_low, count_low = low_counter[0], low_counter[1]  # lowest occurrence

                        comparison_relevance[value_high] = count_high
                        comparison_relevance[value_mid] = count_mid
                        comparison_relevance[value_low] = count_low

                    comparison_targets[target.target_code] = comparison_relevance

                    target_eval_list.clear()
                    comparison_relevance = {}

                comparison_table[goal.id] = comparison_targets
                comparison_targets = {}

            context = {
                'user_sector_eval': user_sector_eval,
                'comparison_table': comparison_table
            }

            data = json.dumps(context, indent=2, default=str)

            return JsonResponse(data, safe=False)

    return render(request, 'survey/comparison.html', content)


@login_required(login_url='login')
def instructions(request):

    return render(request, 'survey/instructions.html')


@login_required(login_url='login')
def comments(request):
    target = Target.objects.filter(target_code = request.POST.get('target_code')).first()
    target_label = target.target_label
    sector_id = request.POST.get('sector_id')

    user_id_list = request.POST.get('user_ids')

    content = {
        'target_code': request.POST.get('target_code'),
        'target_label': target_label,
        'target': target,
        'sector_id': sector_id,
        'user_ids': user_id_list,
    }

    if not user_id_list:  # checking if there are any selected users -> preventing errors
        content['user_select'] = False
    else:
        content['user_select'] = True

    return render(request, 'survey/comments.html', content)


@login_required(login_url='login')
def comment_data(request):
    target = Target.objects.filter(target_code=request.GET.get('target_code')).first()
    target_label = target.target_label
    target_id = target.id

    user_id_list = json.loads(request.GET.get('user_ids'))
    user_ids = user_id_list.split(',')

    num_pos_comments = PredefinedComments.objects.filter(relevance='positive').count()  # 17
    num_comments = PredefinedComments.objects.all().count()                             # 30

    if user_ids[0]:  # checking if there are any selected users -> preventing errors
        users = UserProfile.objects.filter(user_id__in=user_ids)

        prof_background_list = []
        sector_list = []

        for user in users:
            prof_background_list.append(user.prof_background)
            sector_list.append(user.sector)

        # Professional Background Chart
        prof_background_unique = list(Counter(prof_background_list).keys())  # equals to list(set(words))
        prof_background_count = list(Counter(prof_background_list).values())  # counts the elements' frequency

        # Sector Chart
        sector_unique = list(Counter(sector_list).keys())  # equals to list(set(words))
        sector_count = list(Counter(sector_list).values())  # counts the elements' frequency

        # Comment Charts
        comment_list = TargetComment.objects.filter(user_id__in=user_ids,
                                                    target_id=target_id,
                                                    sector_id=request.GET.get('sector_id'))
        positive_comment_list = []
        negative_comment_list = []
        other_comment_list = []

        for comment in comment_list:
            if int(comment.comment_id) <= num_pos_comments:   # 17
                positive_comment = PredefinedComments.objects.get(id=comment.comment_id)
                positive_comment_list.append(positive_comment.comment)

            elif int(comment.comment_id) <= num_comments:     # 30
                negative_comment = PredefinedComments.objects.get(id=comment.comment_id)
                negative_comment_list.append(negative_comment.comment)

            else:
                other_comment = Evaluation.objects.filter(user_id=comment.user_id,
                                                          target_id=target_id,
                                                          sector_id=request.GET.get('sector_id')).first()
                other_comment_list.append(other_comment.note)

        # Positive Comment List
        positive_comment_unique = list(Counter(positive_comment_list).keys())  # equals to list(set(words))
        positive_comment_count = list(Counter(positive_comment_list).values())  # counts the elements' frequency

        positive_comment_index = sorted(range(len(positive_comment_count)), key=lambda k: positive_comment_count[k], reverse=True)   # sorted indexes

        positive_comment_unique = [positive_comment_unique[i] for i in positive_comment_index]  # sorted values
        positive_comment_count = [positive_comment_count[i] for i in positive_comment_index]  # sorted values

        # Negative Comment List
        negative_comment_unique = list(Counter(negative_comment_list).keys())  # equals to list(set(words))
        negative_comment_count = list(Counter(negative_comment_list).values())  # counts the elements' frequency

        negative_comment_index = sorted(range(len(negative_comment_count)), key=lambda k: negative_comment_count[k],
                                        reverse=True)  # sorted indexes

        negative_comment_unique = [negative_comment_unique[i] for i in negative_comment_index]  # sorted values
        negative_comment_count = [negative_comment_count[i] for i in negative_comment_index]  # sorted values

        # Location specific
        loc_spec = Evaluation.objects.filter(user_id__in=user_ids, target_id = target_id,
                                             sector_id = request.GET.get('sector_id')).values_list('location_flag', flat=True)

        loc_spec_true = list(loc_spec).count(True)
        loc_spec_false = list(loc_spec).count(False)

        loc_spec_dic = {
            'true_count': loc_spec_true,
            'false_count': loc_spec_false,
        }

        content = {
            'user_ids': user_ids,
            'prof_background_unique': prof_background_unique,
            'prof_background_count': prof_background_count,

            'sector_unique': sector_unique,
            'sector_count': sector_count,

            'loc_spec': loc_spec_dic,

            'positive_comment_unique': positive_comment_unique,
            'positive_comment_count': positive_comment_count,

            'negative_comment_unique': negative_comment_unique,
            'negative_comment_count': negative_comment_count,

            'other_comments': other_comment_list,
        }

    else:
        content = {}

    data = json.dumps(content, indent=2, default=str)

    return JsonResponse(data, safe=False)

@login_required(login_url='login')
def scores(request):
    sectors = Sector.objects.all()

    content = {
        'sectors': sectors,
    }

    return render(request, 'survey/scores.html', content)