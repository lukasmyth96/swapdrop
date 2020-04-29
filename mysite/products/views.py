from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Product
from matches.models import Like


class ProductListView(ListView):
    model = Product
    template_name = 'products/feed.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_queryset(self):
        """ Returns all products not owned or already liked by currently logged in user"""
        # TODO there's probably an easier way of doing this - do some reading on querysets
        all_products_qs = super().get_queryset()
        other_peoples_products = all_products_qs.exclude(owner=self.request.user)

        my_likes = Like.objects.filter(liked_by=self.request.user)
        already_liked_product_ids = [like.product.id for like in my_likes]

        other_peoples_products_not_already_liked = other_peoples_products.exclude(id__in=already_liked_product_ids)

        return other_peoples_products_not_already_liked


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'products/create_form.html'
    fields = ['name', 'description', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'products/update_form.html'
    fields = ['name', 'description', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.owner:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.owner:
            return True
        return False

