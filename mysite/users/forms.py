from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

from users.validators import is_in_chichester


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        exclude = ['user']


class UserPostcodeForm(forms.ModelForm):
    postcode = forms.CharField(validators=[is_in_chichester])

    class Meta:
        model = Profile
        fields = ['postcode']


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

    def is_initial_valid(self):
        """
        Returns True if initial values passed into form are already valid.

        Used to determine whether or not we need to redirect user to shipping address form after a match.

        Returns
        -------
        is_valid: bool
        """
        try:
            for field_name, field in self.fields.items():
                field.validate(value=self.initial.get(field_name))
        except ValidationError:
            return False

        return True


