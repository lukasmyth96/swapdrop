from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['image', 'image2', 'image3', 'image4', 'name', 'description', 'gender', 'clothing_type', 'size']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}

    def save(self, commit=True):
        self.instance.cropped_dimensions_image = [int(dim) for dim in self.data.get('cropped-dimensions').split(',')]
        self.instance.cropped_dimensions_image2 = [int(dim) for dim in self.data.get('cropped-dimensions').split(',')]
        self.instance.cropped_dimensions_image3 = [int(dim) for dim in self.data.get('cropped-dimensions').split(',')]
        self.instance.cropped_dimensions_image3 = [int(dim) for dim in self.data.get('cropped-dimensions').split(',')]
        return super(ProductCreateForm, self).save(commit=True)


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = ['name', 'description', 'gender', 'clothing_type', 'size']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}

