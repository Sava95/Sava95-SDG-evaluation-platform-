from survey.goals import goals
from survey.models import Target
from survey.models import Goal
import os

# os.system('python manage.py flush')  # resets the database
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_SDG_project.settings")

for goal in goals:
    goal_db = Goal(
        goal_name = goal['name'],
        goal_code = goal['code']
    )

    # goal_db.save()

for index_1, goal in enumerate(goals, start=1):
    for index_2, code in enumerate(goal['target_code']):
        target = Target(
            goal = Goal.objects.get(id=index_1),
            goal_name = goal['name'],
            target_code = code,
            target_label = goal['targets'][index_2]
        )

        # target.save()

