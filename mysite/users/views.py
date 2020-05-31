from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.generic import (
    ListView
)


from products.models import Product

from sizes.models import GenderPreference, GenderOptions, PrimarySize, WaistSize, ShoeSize

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
            messages.success(request, f'Welcome to the swapping revolution.')
            return redirect('profile')
    else:
        user_form = UserRegisterForm()
        postcode_form = UserPostcodeForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'postcode_form': postcode_form})


@login_required()
def profile_info(request):
    if request.method == 'POST':

        # Process gender preference
        selected_gender_values = request.POST.getlist('gender_preference')
        request.user.profile.gender_preference.clear()  # clear existing preferences
        if 'm' in selected_gender_values:
            request.user.profile.gender_preference.add(GenderPreference.objects.get(gender=GenderOptions.MENSWEAR))
        if 'w' in selected_gender_values:
            request.user.profile.gender_preference.add(GenderPreference.objects.get(gender=GenderOptions.WOMENSWEAR))


        # Process primary size selections
        selected_primary_size_ids = [int(_id) for _id in request.POST.getlist('primary_size')]
        selected_primary_sizes = PrimarySize.objects.filter(pk__in=selected_primary_size_ids)
        request.user.profile.primary_sizes.clear()
        request.user.profile.primary_sizes.add(*selected_primary_sizes)

        # Process waist size selections
        selected_waist_size_ids = [int(_id) for _id in request.POST.getlist('waist_size')]
        selected_waist_sizes = WaistSize.objects.filter(pk__in=selected_waist_size_ids)
        request.user.profile.waist_sizes.clear()
        request.user.profile.waist_sizes.add(*selected_waist_sizes)

        # Process shoe sizes
        selected_shoe_size_ids = [int(_id) for _id in request.POST.getlist('shoe_size')]
        selected_shoe_sizes = ShoeSize.objects.filter(pk__in=selected_shoe_size_ids)
        request.user.profile.shoe_sizes.clear()
        request.user.profile.shoe_sizes.add(*selected_shoe_sizes)

        # Process profile pic update
        form = ProfileUpdateForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile')

    else:
        form = ProfileUpdateForm(instance=request.user.profile)

        current_gender_preferences = [str(gender) for gender in request.user.profile.gender_preference.all()]

        context = {'form': form,
                   'current_gender_preferences': current_gender_preferences,
                   'primary_sizes': PrimarySize.objects.all(),
                   'current_primary_size_ids': [str(size.id) for size in request.user.profile.primary_sizes.all()],
                   'waist_sizes': WaistSize.objects.all(),
                   'current_waist_size_ids': [str(size.id) for size in request.user.profile.waist_sizes.all()],
                   'shoe_sizes': ShoeSize.objects.all(),
                   'current_shoe_size_ids': [str(size.id) for size in request.user.profile.shoe_sizes.all()]}

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





