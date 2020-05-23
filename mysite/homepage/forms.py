from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import PotentialUser


class LandingPageForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control register-input',
                                                           'placeholder': 'Email',
                                                           }))

    class Meta:
        model = PotentialUser
        fields = ['email']

