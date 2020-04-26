from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Like
from products.models import Product


def like(request, product_id):

    product = Product.objects.get(pk=product_id)
    like, created_new = Like.objects.get_or_create(liked_by=request.user, product=product)
    if created_new:
        like.save()
        messages.success(request, 'You have liked this product')
    else:
        messages.success(request, 'You have already liked this product')
    return redirect('product-detail', pk=product_id)

