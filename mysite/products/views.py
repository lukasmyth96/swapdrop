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


class ProductListView(ListView):
    model = Product
    template_name = 'products/feed.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_queryset(self):
        """ Returns all products NOT owned by currently logged in user"""
        all_products_qs = super().get_queryset()
        filtered_products_qs = all_products_qs.exclude(owner=self.request.user)
        return filtered_products_qs


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'description']

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

