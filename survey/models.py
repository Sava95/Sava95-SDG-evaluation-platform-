from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    objects = models.Manager()   # to call get function

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    prof_background = models.CharField(max_length= 100)
    sector = models.CharField(max_length= 100)

    class Meta:
        db_table = "user_profile"


class Sector(BaseModel):
    sector_name = models.TextField(max_length = 100)
    sector_code = models.CharField(max_length = 20)
    sector_level = models.CharField(max_length = 10)

    class Meta:
        db_table = "sdg_sectors"


class Goal(BaseModel):
    goal_name = models.CharField(max_length=50)
    goal_code = models.CharField(max_length=10)

    class Meta:
        db_table = "sdg_goals"


class Target(BaseModel):
    goal = models.ForeignKey(Goal, on_delete = models.CASCADE)
    goal_name = models.TextField(max_length = 100)
    target_code = models.CharField(max_length = 10)
    target_label = models.TextField(max_length = 1000)

    class Meta:
        db_table = "sdg_targets"


class EvaluatedGoal(BaseModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    user_name = models.CharField(max_length = 20)
    goal = models.ForeignKey(Goal, on_delete = models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length = 100)
    date_posted = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "evaluated_goals"


class Evaluation(BaseModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    user_name = models.CharField(max_length = 20)
    sector = models.ForeignKey(Sector, on_delete = models.CASCADE)
    target = models.ForeignKey(Target, on_delete = models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete = models.CASCADE)

    relevance = models.CharField(max_length = 10, default=None)
    location_flag = models.BooleanField(default = False)
    note = models.TextField(max_length = 200, default=None)

    date_posted = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "evaluations"


class PredefinedComments(BaseModel):
    comment = models.CharField(max_length = 100, default=None)
    relevance = models.CharField(max_length = 50)

    class Meta:
        db_table = "predefined_comments"


class TargetComment(BaseModel):
    user_id = models.CharField(max_length = 100, default=None)
    user_name = models.CharField(max_length = 100, default=None)

    sector_id = models.CharField(max_length = 100, default = None)
    goal_id = models.CharField(max_length = 100, default = None)
    target_id = models.CharField(max_length = 100, default = None)
    comment_id = models.CharField(max_length = 100, null=True, default = None)

    class Meta:
        db_table = "target_comment"


class SdgCountryValues(BaseModel):
    country = models.CharField(max_length = 100, default=None)
    sdg_goal = models.CharField(max_length = 100, default=None)
    sdg_code = models.CharField(max_length = 100, default=None)
    country_value = models.CharField(max_length = 100, default=None)

    class Meta:
        db_table = "sdg_country_values"


# eSave representative tables
class eSaveCountry(BaseModel):
    country_ID = models.AutoField(primary_key=True, default=None)
    name = models.CharField(max_length=100, default=None)
    short = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = "xxx_country"


class eSaveProjects(BaseModel):
    esave_project_ID = models.AutoField(primary_key=True)
    loan_ID = models.CharField(max_length=100, default=None)

    esave_bank_ID = models.CharField(max_length=100, default=None)
    uskp_sector_ID = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = "xxx_esave_projects"


class eSaveBanks(BaseModel):
    esave_bank_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, default=None)

    country_ID = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = 'xxx_esave_banks'


class eSaveUskpSectors(BaseModel):
    uskp_sector_ID = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, default=None)
    name = models.CharField(max_length=300, default=None)
    parent_sector_group_id = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = 'xxx_uskp_sectors'


class FilesAdmin(BaseModel):
    adminupload = models.FileField(upload_to = 'media')
    title = models.CharField(max_length = 50)

    def __str(self):
        return self.title