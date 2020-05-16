from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.forms import ShippingAddressUpdateForm


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

        if address_form.is_initial_valid():
            # if shipping address already given redirect straight to time slot pick
            messages.success(request, '*shipping address already given - redirect to time slot picker at this point*')
            return redirect('product-feed')
        else:
            # else redirect to shipping address form first
            context = {'address_form': address_form}
            return render(request, 'checkout/shipping_address_redirect.html', context=context)
