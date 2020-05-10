from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView
)

from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ShippingAddressUpdateForm
from products.models import Product
from matches.models import Offer


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account Created! You can now Login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile_info(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(instance=request.user, data=request.POST)
        p_form = ProfileUpdateForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'users/profile_info.html', context=context)


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





