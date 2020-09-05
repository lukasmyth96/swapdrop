import random
from datetime import datetime, timedelta

from django.urls import reverse_lazy
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
from swaps.models import Swap, SwapStatus
from .forms import ProductCreateForm, ProductUpdateForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/feed.html'
    context_object_name = 'products'
    paginate_by = 36
    feed_order_expiry_mins = 30

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

        # 5) shuffle
        filtered_products = list(filtered_products)
        random_seed = self.get_random_seed()
        random.Random(random_seed).shuffle(filtered_products)

        return filtered_products

    def get_random_seed(self):
        time_format = '%d/%m/%y %H:%M:%S'
        random_seed = self.request.session.get('random_seed')
        random_seed_expiry_str = self.request.session.get('random_seed_expiry')
        if (not random_seed) or (datetime.strptime(random_seed_expiry_str, time_format) < datetime.now()):
            random_seed = random.randint(0, 100)
            self.request.session['random_seed'] = random_seed
            self.request.session['random_seed_expiry'] = datetime.strftime(datetime.now() +
                                                                           timedelta(minutes=self.feed_order_expiry_mins), time_format)
        return random_seed


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """
        Overriding to add 'button_text' and 'button_redirect_url' to context.

        This is used in template in the main 'call to action' button which can be on of 4 things depending on status.
        """
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.object
        button_text = ''
        button_redirect_url = '#'
        if product.owner == self.request.user:
            if product.status == ProductStatus.LIVE:
                button_text = f'Review {product.number_of_offers} Offers'
                button_redirect_url = reverse_lazy('review-offers', kwargs={'product_id': product.id})
            elif product.status == ProductStatus.PENDING_CHECKOUT:
                button_text = 'Checkout Now'
                button_redirect_url = reverse_lazy('checkout', kwargs={'product_id': product.id})
        else:
            # get QuerySet of offers made by current user for this product
            users_offers_on_product = Swap.objects.filter(offered_product__owner=self.request.user,
                                                          desired_product=product,
                                                          status=SwapStatus.PENDING_REVIEW)
            if users_offers_on_product:
                button_text = f'Cancel {len(users_offers_on_product)} Offers'
                button_redirect_url = reverse_lazy('cancel-offers', kwargs={'product_id': product.id})
            else:
                button_text = 'Make Offer'
                button_redirect_url = reverse_lazy('make-offer', kwargs={'product_id': product.id})

        context['button_text'] = button_text
        context['button_redirect_url'] = button_redirect_url

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'products/create_form.html'
    success_url = reverse_lazy(viewname='profile-your-items')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'products/update_form.html'
    success_url = reverse_lazy(viewname='profile-your-items')

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
    success_url = reverse_lazy(viewname='profile-your-items')

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.owner:
            return True
        return False

