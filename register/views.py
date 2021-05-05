from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, UserProfileForm


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        profile_form = UserProfileForm(response.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)  # commit=False doesn't save the profile right away
            profile.user = user  # the rest of the data will be saved though form

            if response.POST.get('prof_back'):
                profile.prof_background = response.POST.get('prof_back')
            else:
                profile.prof_background = response.POST.get('professional_background')

            if response.POST.get('sector_other'):
                profile.sector = response.POST.get('sector_other')
            else:
                profile.sector = response.POST.get('Sector')

            profile.save()  # now the profile is saved

            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(response, new_user)   # automatically login after registration

            return redirect("home")
    else:
        form = RegisterForm()
        profile_form = UserProfileForm()

    return render(response, "register/register.html", {"form": form, 'profile_form': profile_form})
