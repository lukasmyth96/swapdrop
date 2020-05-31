from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.generic import (
    ListView
)

from users.forms import UserRegisterForm, UserPostcodeForm, UserUpdateForm, ProfileUpdateForm, ShippingAddressUpdateForm
from products.models import Product
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
            messages.success(request, f'Welcome to the swapping revolution.')
            return redirect('profile')
    else:
        user_form = UserRegisterForm()
        postcode_form = UserPostcodeForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'postcode_form': postcode_form})


@login_required()
def profile_info(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile')

    else:
        form = ProfileUpdateForm(instance=request.user.profile)
        context = {'form': form}
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





