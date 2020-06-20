from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.views.generic import (
    ListView
)


from products.models import Product
from swaps.models import Swap, SwapStatus
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
        self.template_name = 'users/login_mobile.html' if self.request.user_agent.is_mobile else 'users/login.html'
        return super(Login, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.template_name = 'users/login_mobile.html' if self.request.user_agent.is_mobile else 'users/login.html'
        return super(Login, self).post(request, *args, **kwargs)


class ProfileYourItemsListView(ListView):
    model = Product
    template_name = 'users/profile_your_items.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get(self, request, *args, **kwargs):
        """ """
        # Check for and process and timed-out swaps belonging to this user TODO move this logic somewhere else
        users_pending_swaps = Swap.objects.filter((Q(offered_product__owner=self.request.user) | Q(desired_product__owner=self.request.user))
                                                  & Q(status=SwapStatus.PENDING_CHECKOUT))
        for swap in users_pending_swaps:
            if swap.hours_left_to_checkout == 0:
                swap.timeout_reached()
        return super(ProfileYourItemsListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """ Returns all products owned by currently logged in user"""
        all_products = super(ProfileYourItemsListView, self).get_queryset()
        users_products = all_products.filter(owner=self.request.user)
        return users_products


class ProfileOffersMadeListView(ListView):
    model = Product
    template_name = 'users/profile_offers_made.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_queryset(self):
        """ Return all products that currently logged in user has made an offer on"""
        offers_made = Swap.objects.filter(offered_product__owner=self.request.user)
        # making unique list because there can be multiple offers on the same product
        products_bidded_on = list(set([offer.desired_product for offer in offers_made]))
        return products_bidded_on


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
            return redirect('profile-your-items')

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


def shipping_address_info(request):

    if request.method == 'POST':
        address_form = ShippingAddressUpdateForm(instance=request.user.profile, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, 'Your shipping address has been updated')
            return redirect('profile-your-items')

    else:
        address_form = ShippingAddressUpdateForm(instance=request.user.profile)
        context = {'address_form': address_form}
        return render(request, 'users/shipping_address_info.html', context=context)


def profile_other_user(request, user_id):
    """ View for viewing another users profile """
    try:
        user = User.objects.get(id=user_id)
        products = Product.objects.filter(owner=user)
        context = {'other_user': user,
                   'products': products}
        return render(request, template_name='users/profile_other_user.html', context=context)
    except User.DoesNotExist:
        raise Http404('Oops - this user doesn\'t exist')







