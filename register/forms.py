from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from survey.models import UserProfile

educational_background = (
    ('', 'Choose...'),
    ('Financial/commercial/banking', 'Financial/commercial/banking'),
    ('Technical/engineering', 'Technical/engineering'),
    ('Environmental/sustainability', 'Environmental/sustainability'),
    ('Other', 'Other')
)

sector_of_employer = (
    ('', 'Choose...'),
    ('Industrial/manufacturing', 'Industrial/manufacturing'),
    ('Commercial/banking', 'Commercial/banking'),
    ('Transport', 'Transport'),
    ('Consulting', 'Consulting'),
    ('Science/research', 'Science/research'),
    ('Other', 'Other')
)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User

        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


class UserProfileForm(ModelForm):

    professional_background = forms.ChoiceField(choices=educational_background)
    Sector = forms.ChoiceField(choices=sector_of_employer)

    class Meta:
        model = UserProfile

        fields = ['professional_background', 'Sector']

# needs to be named Meta, with the names of the variables as specified
# model - defines what we are going to change, fields - defines the order of which it is going to be displayed
# fields will save the variable in personal info as long as the variables have the same name (first_name,email,...)
