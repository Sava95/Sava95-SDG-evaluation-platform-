from survey.models import Goal
from survey.models import Target

Goals = Goal.objects.all()
Targets = Target.objects.all()

table = {}

for goal in Goals:
    table[goal.id] = Target.objects.filter(goal_id = goal.id)

for goal in Goals:
    for item in table[goal.id]:
        print(item)

    print('==============================================================')

