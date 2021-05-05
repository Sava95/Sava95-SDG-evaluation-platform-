import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_SDG_project.settings")
django.setup()

from survey.models import User, Goal, Target, Sector, EvaluatedGoal, Evaluation

with open('data.txt') as json_file:
    data = json.load(json_file)

print(data)

# Importing data into Database
print(data['goals'])

# Filling in the Evaluation Goal Table
for sdg in data['goals']:
    evaluated_goal = EvaluatedGoal()

    user = User.objects.filter(first_name=data['name']).first()
    goal = Goal.objects.get(id = data['goals'][sdg]['goal_id'])
    sector = Sector.objects.filter(sector_code = data['sector_code']).first()

    evaluated_goal.user_id = user.id
    evaluated_goal.user_name = user.first_name
    evaluated_goal.goal_id = goal.id
    evaluated_goal.goal_name = goal.goal_name
    evaluated_goal.sector_id = sector.id

    # Filling in the Evaluation Table
    for target in data['goals'][sdg]['targets']:
        evaluation = Evaluation()

        target_obj = Target.objects.filter(target_code = data['goals'][sdg]['targets'][target]['target_code']).first()

        evaluation.user_id = user.id
        evaluation.user_name = user.first_name
        evaluation.sector_id = sector.id
        evaluation.goal_id = goal.id
        evaluation.target_id = target_obj.id
        evaluation.relevance = data['goals'][sdg]['targets'][target]['target_relevance']
        evaluation.location_flag = 0
        evaluation.note = ''

        evaluation.save()
    evaluated_goal.save()


