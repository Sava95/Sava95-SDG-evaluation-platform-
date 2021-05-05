from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from survey.models import Evaluation, User, Target, Goal
from .serializers import UserSerializer, YourSerializer
from django.http import JsonResponse
import json


class SdgScoreApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        sector_id = 63

        SDG_scores = {}

        for index, goal in enumerate(Goal.objects.all(), 1):
            relevance = []
            target_relevance = []

            target_list_ids = Target.objects.filter(goal_id = goal.id).values_list('pk', flat=True)

            target_relevance = list(Evaluation.objects.filter(sector_id = sector_id,
                                                              goal_id = goal.id,
                                                              target_id__in = target_list_ids).values_list('relevance', flat=True))

            target_count = len(target_relevance)
            positive_relevance_count = target_relevance.count('positive')
            negative_relevance_count = target_relevance.count('negative')

            if positive_relevance_count != 0:
                relevance = round(positive_relevance_count-negative_relevance_count/target_count, 2)
            else:
                relevance = 0

            SDG_scores.setdefault("SDG_" + str(index), {})['relevance'] = {}  # creates an empty ['relevance'] nested list
            SDG_scores["SDG_" + str(index)]['relevance'] = relevance

        # results = ScoreSerializer(SDG_scores, many=True).data
        # results = json.JSONEncoder(indent=4).encode(SDG_scores)

        return Response(SDG_scores)

        # return JsonResponse(SDG_scores, safe=False)

        # yourdata = {"likes": 10, "comments": 0}
        # results = YourSerializer(yourdata, many=True).data
        # return Response(results)

        #
        # users = User.objects.all()
        # results = UserSerializer(users, many=True).data
        #
        # return Response(results)

