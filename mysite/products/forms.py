from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['image', 'image2', 'image3', 'image4', 'name', 'description', 'gender', 'clothing_type', 'size']
        widgets = {'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'e.g only worn a few times, true to size'}),
                   'name': forms.TextInput(attrs={'placeholder': 'e.g. White Nike Jumper'})}

    def save(self, commit=True):
        self.instance.crop_dimensions_image = self.extract_crop_dims_from_post_data('crop_dimensions_image')
        self.instance.crop_dimensions_image2 = self.extract_crop_dims_from_post_data('crop_dimensions_image2')
        self.instance.crop_dimensions_image3 = self.extract_crop_dims_from_post_data('crop_dimensions_image3')
        self.instance.crop_dimensions_image4 = self.extract_crop_dims_from_post_data('crop_dimensions_image4')
        return super(ProductCreateForm, self).save(commit=True)

    def extract_crop_dims_from_post_data(self, field_name):
        try:
            dims = [int(dim) for dim in self.data.get(field_name).split(',')]
        except ValueError:
            dims = None  # means no image was uploaded for this field

        return dims


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = ['name', 'description', 'gender', 'clothing_type', 'size']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}

