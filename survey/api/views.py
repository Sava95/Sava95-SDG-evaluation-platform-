from _pytest.assertion.util import isset
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from rest_framework import permissions
from survey.models import Evaluation, Sector, Target, Goal, SdgCountryValues, eSaveCountry, eSaveProjects, eSaveBanks, \
    eSaveUskpSectors, SoF


class SdgScoreApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Input parameters
        if request.GET.get('project_id'):
            # ================================ 1. End-point: Project ID ================================ #

            project_id = request.GET.get('project_id')

            try:
                # Country Name
                esave_bank_ID = eSaveProjects.objects.get(esave_project_ID=project_id).esave_bank_ID
                country_ID = eSaveBanks.objects.get(esave_bank_ID=esave_bank_ID).country_ID
                country_name = eSaveCountry.objects.get(country_ID=country_ID).name
                bank_name = eSaveBanks.objects.get(esave_bank_ID=esave_bank_ID).name

                # Sector ID
                uskp_sector_ID = eSaveProjects.objects.get(esave_project_ID=project_id).uskp_sector_ID
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
                    index = numbers.index(str(uskp_parent_sector_group_id))
                    sector_code = letters[index] + str(uskp_code)

                sector_id = Sector.objects.get(sector_code=sector_code).id
                country = country_name

            except Exception as e:
                Message = {
                    'message': 'The SDG score is not available for this project',
                    'error': str(e)
                }

                return Response(Message)

        elif request.GET.get('loan_id'):
            # ================================ 2. End-point: Loan ID + Bank Name ================================ #
            loan_id = request.GET.get('loan_id')
            bank_name = request.GET.get('bank_name')

            try:
                # Country Name
                country_ID = eSaveBanks.objects.get(name=bank_name).country_ID
                country_name = eSaveCountry.objects.get(country_ID=country_ID).name

                # Sector ID
                bank_id = eSaveBanks.objects.get(name=bank_name).esave_bank_ID
                uskp_sector_ID = eSaveProjects.objects.get(loan_ID=loan_id, esave_bank_ID=bank_id).uskp_sector_ID
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
                    index = numbers.index(str(uskp_parent_sector_group_id))
                    sector_code = letters[index] + str(uskp_code)

                sector_id = Sector.objects.get(sector_code=sector_code).id
                country = country_name

            except Exception as e:
                Message = {
                    'message': 'The SDG score is not available for this project',
                    'error': str(e),
                    'bank_name': bank_name
                }

                return Response(Message)

        else:
            # ================================ 3. End-point: Bank Name + SoF + Date ================================ #
            bank_id = request.GET.get('bank')
            sof_id = request.GET.get('sof')
            date_from = request.GET.get('date1')
            date_to = request.GET.get('date2')

            try:
                # Bank Name
                bank_name = eSaveBanks.objects.get(esave_bank_ID=bank_id).name

                # Country Name
                country_ID = eSaveBanks.objects.get(esave_bank_ID=bank_id).country_ID
                country = eSaveCountry.objects.get(country_ID=country_ID).name

                # Project list
                project_list = eSaveProjects.objects.filter(esave_bank_ID=bank_id, esave_source_of_fund_ID = sof_id,
                                                            create_datetime__range=[date_from, date_to])

                # Sector code check
                numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                           '18', '19', '20', '21']
                letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U']

                sector_id_list = []
                loan_amount_list = []

                for project in project_list:
                    uskp_sector_ID = project.uskp_sector_ID

                    if uskp_sector_ID is not None:  # checking to see if the sector has a uskp sector id
                        uskp_sector = eSaveUskpSectors.objects.get(uskp_sector_ID=uskp_sector_ID)
                        uskp_code = uskp_sector.code
                        uskp_parent_sector_group_id = uskp_sector.parent_sector_group_id

                        if uskp_code in letters:
                            sector_code = uskp_code + str(uskp_parent_sector_group_id)
                        else:
                            index = numbers.index(str(uskp_parent_sector_group_id))
                            sector_code = letters[index] + str(uskp_code)

                        if Sector.objects.filter(sector_code=sector_code):  # if there are sectors with sector_code
                            sector_id = Sector.objects.get(sector_code=sector_code).id
                            sector_id_list.append(sector_id)

                            del sector_id

                            # Calculating sector loan amount
                            loan_amount = int(project.loan_amount)/int(project.loan_amount_exchange_rate_euro)
                            loan_amount_list.append(loan_amount)

                sector_unique_id_list = list(set(sector_id_list))  # find unique sectors
                total_loan_amount = sum(loan_amount_list)

            except Exception as e:
                Message = {
                    'message': 'The SDG score is not available for this project',
                    'error': str(e),
                    'date_from': date_from,
                    'date_to': date_to,
                }

                return Response(Message)

        # ================================== Calculation ==================================
        SDG_scores = {}

        relevance_list = []
        weighed_relevance_list = []

        relevance_sector_list = []
        weighed_relevance_sector_list = []

        sdg_country_value_list = []

        for index, goal in enumerate(Goal.objects.all(), 1):   # calculates the relevance for each goal
            target_list_ids = Target.objects.filter(goal_id=goal.id).values_list('pk', flat=True)

            try:
                if sector_id_list:
                    for index_2, sector_id in enumerate(sector_id_list):
                        target_relevance = list(Evaluation.objects.filter(sector_id=sector_id,
                                                                          goal_id=goal.id,
                                                                          target_id__in=target_list_ids).values_list('relevance', flat=True))

                        target_count = len(target_relevance)
                        positive_relevance_count = target_relevance.count('positive')
                        negative_relevance_count = target_relevance.count('negative')

                        if (positive_relevance_count - negative_relevance_count) != 0:
                            relevance = round((positive_relevance_count - negative_relevance_count) / target_count, 2)
                        else:
                            relevance = 0

                        relevance_sector_list = relevance_sector_list.append(relevance)   # list of relevance's per sector
                        # weighed_relevance = relevance * loan_amount[index_2]/total_loan_amount

                        # weighed_relevance_sector_list = weighed_relevance_sector_list.append(weighed_relevance)

                    sdg_code = str("SDG_" + str(index))

                    SDG_scores.setdefault(sdg_code, {})['relevance'] = {}  # creates an empty ['relevance'] nested list
                    SDG_scores.setdefault(sdg_code, {})['weighted_relevance'] = {}  # creates an empty ['relevance'] nested list

                    SDG_scores[sdg_code]['relevance'] = sum(relevance_sector_list)/len(relevance_sector_list)
                    # SDG_scores[sdg_code]['weighted_relevance'] = sum(weighed_relevance_sector_list)

                elif isset('sector_id'):  # 1. or 2. end point
                    target_relevance = list(Evaluation.objects.filter(sector_id=sector_id,
                                                                      goal_id=goal.id,
                                                                      target_id__in=target_list_ids).values_list('relevance',
                                                                                                                 flat=True))
                    target_count = len(target_relevance)
                    positive_relevance_count = target_relevance.count('positive')
                    negative_relevance_count = target_relevance.count('negative')

                    if (positive_relevance_count - negative_relevance_count) != 0:
                        relevance = round((positive_relevance_count - negative_relevance_count) / target_count, 2)
                    else:
                        relevance = 0

                    sdg_code = str("SDG_" + str(index))

                    SDG_scores.setdefault(sdg_code, {})['relevance'] = {}  # creates an empty ['relevance'] nested list
                    SDG_scores[sdg_code]['relevance'] = relevance

                else:
                    Message = {
                        'message': 'There are no projects',
                    }

                    return Response(Message)

                try:   # country specific parameters
                    sdg_country_object = SdgCountryValues.objects.filter(sdg_code=sdg_code, country=country)[0]
                    sdg_factor = getattr(sdg_country_object, 'country_value_2021')
                    sdg_country_value = round(min(1, relevance * (int(sdg_factor) + 1)), 2)

                except:
                    sdg_country_value = relevance

                SDG_scores[sdg_code]['sdg_country_value'] = sdg_country_value

                relevance_list.append(relevance)
                sdg_country_value_list.append(sdg_country_value)

                # if sector_id_list:
                #     weighed_relevance_list.append(SDG_scores[sdg_code]['weighted_relevance'])

            except Exception as e:
                Message = {
                    'message': 'The SDG score is not available for this project',
                    'error': str(e),
                }

                return Response(Message)

        content = {
            'relevance_list': relevance_list,
            'weighed_relevance_list': weighed_relevance_list,
            'bank_name': bank_name,
            'sdg_country_value_list': sdg_country_value_list,
            'total_loan_amount': total_loan_amount,
            'loan_amount_list': loan_amount_list,
            'country': country,
        }
        sector_name_list = []
        sector_code_list = []

        if sector_id_list:   # if 3.end point
            for sector_id_in_list in sector_id_list:
                sector_name = Sector.objects.get(id = sector_id_in_list).sector_name,
                sector_code = Sector.objects.get(id = sector_id_in_list).sector_code,

                sector_name_list.append(sector_name)
                sector_code_list.append(sector_code)

            content['sector_name'] = sector_name_list,
            content['sector_code'] = sector_code_list,

        else:
            content['sector_name'] = Sector.objects.get(id=sector_id).sector_name,
            content['sector_code'] = Sector.objects.get(id=sector_id).sector_code,

        return render(request, 'survey/relevance_result.html', content)

    # return Response(SDG_scores)
