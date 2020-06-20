from enum import Enum

from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect

from products.models import Product


def owns_product(view_func):
    """ Decorator for checkout views to ensure that the logged in user owns the product """
    def wrapper(request, product_id, *args, **kwargs):
        product = Product.objects.get(id=product_id)
        if product:
            if product.owner == request.user:
                return view_func(request, product_id, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        else:
            return Http404()

    return wrapper


class CheckoutStatus(Enum):
    """ Must be in order!"""
    CHECKOUT_STARTED = 0
    ADDRESS_GIVEN = 1
    TIMESLOT_PICKED = 2
    CHECKOUT_COMPLETE = 3


def verify_checkout_progress(required_checkout_status):
    """
    Decorator that checks that the uses django sessions to verify that the user has completed the required previous
    stages in the checkout process."
    Parameters
    ----------
    required_checkout_status: CheckoutStatus
    """
    def wrapper1(view_func):
        def wrapper2(request, product_id, *args, **kwargs):
            product_checkout_status_str = request.session.get('checkout_status', {}).get(str(product_id))
            if product_checkout_status_str and product_checkout_status_str == required_checkout_status.name:
                return view_func(request, product_id, *args, **kwargs)
            else:
                return redirect('checkout', product_id=product_id)
        return wrapper2
    return wrapper1
