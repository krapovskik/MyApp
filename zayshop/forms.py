from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.forms import DateInput


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phonenumber', 'birthdate', 'location', 'facebook', 'instagram']
        widgets = {
            'birthdate': DateInput(attrs={'type': 'date'}),
        }
