from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from survey.models import Evaluation, Sector, Target, Goal, SdgCountryValues, eSaveCountry, eSaveProjects, eSaveBanks, eSaveUskpSectors


class SdgScoreApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Input parameters
        if request.GET.get('project_id'):
            # 1. End-point: Project ID
            project_id = request.GET.get('project_id')

            try:
                # Country Name
                esave_bank_ID = eSaveProjects.objects.get(esave_project_ID = project_id).esave_bank_ID
                country_ID = eSaveBanks.objects.get(esave_bank_ID = esave_bank_ID).country_ID
                country_name = eSaveCountry.objects.get(country_ID = country_ID).name

                # Sector ID
                uskp_sector_ID = eSaveProjects.objects.get(esave_project_ID = project_id).uskp_sector_ID
                uskp_sector = eSaveUskpSectors.objects.get(uskp_sector_ID = uskp_sector_ID)

                uskp_code = uskp_sector.code
                uskp_parent_sector_group_id = uskp_sector.parent_sector_group_id

                # Sector code check
                numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
                letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U']

                if uskp_code in letters:
                    sector_code = uskp_code + str(uskp_parent_sector_group_id)
                else:
                    index = numbers.index(str(uskp_parent_sector_group_id))
                    sector_code = letters[index] + str(uskp_code)

                sector_id = Sector.objects.get(sector_code = sector_code).id
                country = country_name

            except Exception as e:
                Message = {
                    'message': 'The SDG score is not available for this project',
                    'error': str(e)
                    }

                return Response(Message)

        else:
            # 2. End-point: Loan ID + Bank Name
            loan_id = request.GET.get('loan_id')
            bank_name = request.GET.get('bank_name')

            try:
                # Country Name
                country_ID = eSaveBanks.objects.get(name= bank_name).country_ID
                country_name = eSaveCountry.objects.get(country_ID = country_ID).name

                # Sector ID
                bank_id = eSaveBanks.objects.get(name= bank_name).esave_bank_ID
                uskp_sector_ID = eSaveProjects.objects.get(loan_ID = loan_id, esave_bank_ID = bank_id).uskp_sector_ID
                uskp_sector = eSaveUskpSectors.objects.get(uskp_sector_ID=uskp_sector_ID)

                uskp_code = uskp_sector.code
                uskp_parent_sector_group_id = uskp_sector.parent_sector_group_id

                # Sector code check
                numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                           '18', '19', '20', '21']
                letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U']

                if uskp_code in letters:
                    sector_code = uskp_code + str(uskp_parent_sector_group_id)
                else:
                    index = numbers.index(uskp_code)
                    sector_code = letters[index] + str(uskp_parent_sector_group_id)

                sector_id = Sector.objects.get(sector_code=sector_code).id
                country = country_name

            except Exception as e:
                Message = {
                    'message': 'The SDG score is not available for this project',
                    'error': str(e),
                    }

                return Response(Message)

        SDG_scores = {}

        # Calculation
        for index, goal in enumerate(Goal.objects.all(), 1):
            target_list_ids = Target.objects.filter(goal_id = goal.id).values_list('pk', flat=True)

            target_relevance = list(Evaluation.objects.filter(sector_id = sector_id,
                                                              goal_id = goal.id,
                                                              target_id__in = target_list_ids).values_list('relevance', flat=True))

            target_count = len(target_relevance)
            positive_relevance_count = target_relevance.count('positive')
            negative_relevance_count = target_relevance.count('negative')

            if (positive_relevance_count-negative_relevance_count) != 0:
                relevance = round((positive_relevance_count-negative_relevance_count)/target_count, 2)
            else:
                relevance = 0

            sdg_code = str("SDG_" + str(index))

            SDG_scores.setdefault(sdg_code, {})['relevance'] = {}  # creates an empty ['relevance'] nested list
            SDG_scores[sdg_code]['relevance'] = relevance

            try:
                sdg_country_object = SdgCountryValues.objects.filter(sdg_code = sdg_code, country = country)[0]
                sdg_factor = getattr(sdg_country_object, 'country_value')
                sdg_country_value = round(min(1, relevance * (int(sdg_factor) + 1)), 2)

            except:
                sdg_country_value = 'Not Available'

            SDG_scores[sdg_code]['sdg_country_value'] = sdg_country_value

        return Response(SDG_scores)