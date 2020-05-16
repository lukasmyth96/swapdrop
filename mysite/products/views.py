from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Product, ProductStatus
from swaps.models import Swap
from .forms import ProductCreateForm, ProductUpdateForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/feed.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_queryset(self):
        """ Returns all LIVE (non-matched) products the current user does not own and hasn't already made an offer for"""

        live_products = Product.objects.filter(status=ProductStatus.LIVE)  # Get QuerySet of all LIVE products
        other_peoples_products = live_products.exclude(owner=self.request.user)  # Filter products owned by me

        # Get set of product ids for products I've already made an offer on (so don't want to see in my feed again)
        my_offers = Swap.objects.filter(offered_product__owner__exact=self.request.user)
        already_offered_on_product_ids = set([offer.desired_product.id for offer in my_offers])

        # Get other peoples products I've not already made an offer of
        other_peoples_products_not_already_offered_for = other_peoples_products.exclude(id__in=already_offered_on_product_ids)

        return other_peoples_products_not_already_offered_for


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'products/create_form.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'products/update_form.html'
    success_url = '/profile'

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
    success_url = '/profile'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.owner:
            return True
        return False

