from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['image', 'name', 'description', 'gender', 'clothing_type', 'size']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}

    def save(self, commit=True):
        print('stop here')
        self.instance.cropped_dimensions = [int(dim) for dim in self.data.get('cropped-dimensions').split(',')]
        super(ProductCreateForm, self).save(commit=True)


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = ['image', 'name', 'description', 'gender', 'clothing_type', 'size']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}

