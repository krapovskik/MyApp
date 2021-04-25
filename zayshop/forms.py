from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.forms import DateInput


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phonenumber', 'birthdate', 'location', 'facebook', 'instagram']
        widgets = {
            'birthdate': DateInput(attrs={'type': 'date'}),
        }


class EmailForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
