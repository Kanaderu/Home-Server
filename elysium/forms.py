from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('city', 'state', 'gender')


# User Registration Forms
class RegisterForm(UserCreationForm):
    #user_type = forms.ChoiceField(choices=UserInfo.USER_TYPE, help_text="User Account Type")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', )
