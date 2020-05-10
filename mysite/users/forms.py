from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class ShippingAddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['image', 'user']  # ie include all fields except image (house_name_number, address...)
        labels = {'house_name_number': 'House Name/Number',  # django automates this. override bad ones.
                  'address_line_1': 'Address Line 1',
                  'address_line_2': 'Address Line 2',
                  'town_city': 'Town/City',
                  'contact_number': 'Contact Number'
                  }

    def __init__(self, *args, **kwargs):
        super(ShippingAddressUpdateForm, self).__init__(*args, **kwargs)
        self.fields['house_name_number'].required = True
        self.fields['address_line_1'].required = True
        self.fields['town_city'].required = True
        self.fields['postcode'].required = True
        self.fields['contact_number'].required = True
