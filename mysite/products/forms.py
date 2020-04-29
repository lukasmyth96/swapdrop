from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'image']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'image']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}

