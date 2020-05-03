from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpResponse

from .models import Like
from products.models import Product


def like(request, product_id):

    product = Product.objects.get(pk=product_id)
    _like, created_new = Like.objects.get_or_create(liked_by=request.user, product=product)
    if created_new:
        _like.save()
        messages.success(request, 'You have liked this product')
        return redirect('make-offer', product_id=product_id)
    else:
        messages.success(request, 'You have already liked this product')
        return redirect('product-detail', product_id=product_id)


class MakeOfferListView(ListView):
    model = Product
    template_name = 'matches/make_offer.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get(self, request, product_id=None, *args, **kwargs):
        return super(MakeOfferListView, self).get(request)

    def post(self, request, product_id):
        selected_product_ids = [int(_id) for _id in request.POST.getlist('image-picker-select')]
        return HttpResponse('Selected product ids are {}'.format(selected_product_ids))

    def get_queryset(self):
        """ Returns all products owned by currently logged in user"""
        all_products = super().get_queryset()
        users_products = all_products.filter(owner=self.request.user)
        return users_products



