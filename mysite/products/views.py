from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Product, ProductStatus
from sizes.model_enums import GenderOptions
from swaps.models import Swap
from .forms import ProductCreateForm, ProductUpdateForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/feed.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_queryset(self):
        """ Returns all LIVE (non-matched) products the current user does not own and hasn't already made an offer for"""

        # 1) Filter for LIVE products only
        filtered_products = Product.objects.filter(status=ProductStatus.LIVE)

        # 2) Exclude products current user owns
        filtered_products = filtered_products.exclude(owner=self.request.user)

        # 3) Filter by current users gender preference
        users_gender_preference = self.request.user.profile.gender_preference
        if users_gender_preference not in [GenderOptions.UNISEX, None]:
            filtered_products = filtered_products.filter(gender__in=[users_gender_preference, GenderOptions.UNISEX])

        # 4) Exclude products current user has made offer on already
        users_offers = Swap.objects.filter(offered_product__owner__exact=self.request.user)
        already_offered_on_product_ids = set([offer.desired_product.id for offer in users_offers])
        filtered_products = filtered_products.exclude(id__in=already_offered_on_product_ids)

        return filtered_products


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
        return super(ProductCreateView, self).form_valid(form)


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

