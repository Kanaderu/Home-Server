from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .forms import UserForm, ProfileForm, RegisterForm
from django.utils.translation import gettext as _


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            #return redirect('settings:profile')
            return redirect('profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# User Registration Views
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():# and profile_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()

            #profile_form = ProfileForm(request.POST, instance=request.user.profile)
            profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
            profile_form.save()
            # add userinfo data
#            user.userinfo.user_type = register_form.cleaned_data.get('user_type')
            user.save()
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        register_form = RegisterForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {
        'register_form': register_form,
        'profile_form': profile_form,
    })
