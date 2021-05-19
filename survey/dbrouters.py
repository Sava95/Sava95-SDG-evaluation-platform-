from survey.models import eSaveCountry, eSaveProjects, eSaveBanks, eSaveUskpSectors


class MyDBRouter(object):
    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        esave2_prod_models = [eSaveCountry, eSaveProjects, eSaveBanks, eSaveUskpSectors]

        if model in esave2_prod_models:
            return 'esave'

        return None

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        esave2_prod_models = [eSaveCountry, eSaveProjects, eSaveBanks, eSaveUskpSectors]

        if model in esave2_prod_models:
            return 'esave'

        return None