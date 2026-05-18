from django import forms
from django.contrib.auth.models import User
from .models import PanditProfile

class PanditRegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']



class PanditProfileForm(forms.ModelForm):
    class Meta:
        model = PanditProfile
        fields = ['photo', 'state', 'city', 'experience', 'expertise', 'fees']
