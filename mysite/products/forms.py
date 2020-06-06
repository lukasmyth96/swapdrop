from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['image', 'name', 'description', 'gender', 'clothing_type', 'size']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = ['image', 'name', 'description', 'gender', 'clothing_type', 'size']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}

