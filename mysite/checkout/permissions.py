from django.http import HttpResponseForbidden, Http404

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
