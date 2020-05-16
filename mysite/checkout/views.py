from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.forms import ShippingAddressUpdateForm


@login_required()
def checkout(request):
    """
    Entry-point for all checkouts - redirects to shipping-address-redirect if address not already given otherwise
    redirects to time-slot picker.
    """
    address_form = ShippingAddressUpdateForm(instance=request.user.profile)
    if address_form.is_initial_valid():
        # if shipping address already given redirect straight to time slot pick
        messages.success(request, 'shipping address already given')
        return redirect('pick-collection-time')
    else:
        return redirect('shipping-address-redirect')


@login_required()
def shipping_address_redirect(request):

    if request.method == 'POST':
        address_form = ShippingAddressUpdateForm(instance=request.user.profile, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, '*will be redirected to time slot picker at this point*')
            return redirect('product-feed')
    else:
        address_form = ShippingAddressUpdateForm(instance=request.user.profile)
        return render(request, 'checkout/shipping_address_redirect.html', context={'address_form': address_form})


@login_required()
def pick_collection_time(request):
    return render(request, template_name='checkout/pick_collection_time.html')
