from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.views.generic import (
    ListView
)


from products.models import Product

from sizes.models import Size
from sizes.model_enums import GenderOptions, SizeTypes

from users.forms import UserRegisterForm, UserPostcodeForm, UserUpdateForm, ProfileUpdateForm, ShippingAddressUpdateForm
from users.models import Profile


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        postcode_form = UserPostcodeForm(request.POST)
        if user_form.is_valid() and postcode_form.is_valid():
            # Create new user and profile
            user = user_form.save()
            # Note - there's probably an easier way of doing below
            profile = Profile.objects.get(user=user)
            profile.postcode = postcode_form.cleaned_data.get('postcode')
            profile.save(update_fields=['postcode'])

            # Automatically log user in
            user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password1'])
            login(request, user)
            messages.success(request, f'Welcome to Swapdrop - please selected your preferences below...')
            return redirect('profile-info')
    else:
        user_form = UserRegisterForm()
        postcode_form = UserPostcodeForm()

    template = 'users/register_mobile.html' if request.user_agent.is_mobile else 'users/register.html'
    return render(request, template, {'user_form': user_form, 'postcode_form': postcode_form})


class Login(auth_views.LoginView):

    def __init__(self, *args, **kwargs):
        """ Overriding base LoginView to make template name different for mobile/desktop"""
        super(Login, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.template_name = 'users/login_mobile.html' if request.user_agent.is_mobile else 'users/login.html'
        return super(Login, self).get(request, *args, **kwargs)





@login_required()
def profile_info(request):
    if request.method == 'POST':

        # Process gender preference
        selected_gender_value = request.POST.get('gender_preference')
        if selected_gender_value == 'm':
            request.user.profile.gender_preference = GenderOptions.MENSWEAR
        elif selected_gender_value == 'w':
            request.user.profile.gender_preference = GenderOptions.WOMENSWEAR
        request.user.profile.save(update_fields=['gender_preference'])

        # Process size selections
        # combine selected Size ids from each of the three dropdowns
        selected_size_ids = request.POST.getlist('primary_size') + request.POST.getlist('waist_size') + request.POST.getlist('shoe_size')
        selected_size_ids = [int(_id) for _id in selected_size_ids]
        selected_sizes = Size.objects.filter(pk__in=selected_size_ids)
        request.user.profile.sizes.clear()
        request.user.profile.sizes.add(*selected_sizes)

        # Process profile pic update
        form = ProfileUpdateForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile')

    else:
        form = ProfileUpdateForm(instance=request.user.profile)

        current_gender_preference = request.user.profile.gender_preference
        current_gender_preference_str = '' if current_gender_preference is None else current_gender_preference.name

        context = {'form': form,
                   'current_gender_preference': current_gender_preference_str,
                   'primary_sizes': Size.objects.filter(size_type=SizeTypes.PRIMARY),
                   'current_primary_size_ids': [str(size.id) for size in request.user.profile.sizes.filter(size_type=SizeTypes.PRIMARY)],
                   'waist_sizes': Size.objects.filter(size_type=SizeTypes.WAIST),
                   'current_waist_size_ids': [str(size.id) for size in request.user.profile.sizes.filter(size_type=SizeTypes.WAIST)],
                   'shoe_sizes': Size.objects.filter(size_type=SizeTypes.SHOE),
                   'current_shoe_size_ids': [str(size.id) for size in request.user.profile.sizes.filter(size_type=SizeTypes.SHOE)]}

        return render(request, 'users/profile_info.html', context=context)


@login_required()
def shipping_address_info(request):

    if request.method == 'POST':
        address_form = ShippingAddressUpdateForm(instance=request.user.profile, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, 'Your shipping address has been updated')
            return redirect('profile')

    else:
        address_form = ShippingAddressUpdateForm(instance=request.user.profile)
        context = {'address_form': address_form}
        return render(request, 'users/shipping_address_info.html', context=context)


class ProfileProductsListView(ListView):
    model = Product
    template_name = 'users/profile.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_queryset(self):
        """ Returns all products owned by currently logged in user"""
        all_products = super().get_queryset()
        users_products = all_products.filter(owner=self.request.user)
        return users_products





