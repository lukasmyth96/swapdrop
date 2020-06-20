from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView

from products.models import Product, ProductStatus
from swaps.model_enums import SwapStatus
from swaps.models import Swap


class MakeOfferListView(ListView):
    model = Product
    template_name = 'swaps/make_offer.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get(self, request, product_id=None, *args, **kwargs):
        return super(MakeOfferListView, self).get(request)

    def get_queryset(self):
        """ Returns all products owned by currently logged in user"""
        all_products = super().get_queryset()
        users_products = all_products.filter(owner=self.request.user, status=ProductStatus.LIVE)
        return users_products

    def post(self, request, product_id):
        """
        Process submission of 'make offer' form. Redirect to form.

        Extracts list of offered product ids, creates and saves Offer objects for each offer and then redirects user
        back to feed

        Parameters
        ----------
        request
        product_id: int
            id of the desired product
        """

        # Extract ids of selected products from the select box in the form
        # FIXME probably a more reliable way of doing this?
        product_id_strings = list(request.POST.keys())[1:]  # gets list of product ids that have been selected
        selected_product_ids = [int(prod_id) for prod_id in product_id_strings]  # converts each to a int

        # Show warning if no items have been offered
        if not selected_product_ids:
            messages.warning(request, 'You must select at least one item to offer')
            return redirect('make-offer', product_id=product_id)

        # Construct objects for offered products and desired product
        offered_products = [Product.objects.get(pk=product_id) for product_id in selected_product_ids]
        desired_product = Product.objects.get(pk=product_id)

        # Create and save offer objects
        for offered_product in offered_products:
            _swap, created_new = Swap.objects.get_or_create(offered_product=offered_product, desired_product=desired_product)
            if created_new:
                _swap.save()

        messages.success(request, 'Your offer has been sent')
        return redirect('product-feed')


class ReviewOffersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Product
    template_name = 'swaps/review_offers.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_queryset(self):
        """ Returns list of all products that have been offered for current product"""

        if self.users_product.status == ProductStatus.LIVE:
            offers_for_product = Swap.objects.filter(desired_product=self.users_product,
                                                     status=SwapStatus.PENDING_REVIEW)
            offered_products = [offer.offered_product for offer in offers_for_product]
        else:
            offered_products = []
            messages.warning(self.request, 'You have already accepted an offer on this product')

        return offered_products

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Add users_product to context so URLs can be created for links to review_single_offer
        FIXME - this probably isn't needed but can't get to work by getting users_product_id directly in template
        """
        context = super(ReviewOffersListView, self).get_context_data(object_list=object_list, **kwargs)
        context['users_product'] = self.users_product
        return context

    @property
    def users_product(self):
        users_product_id = self.kwargs.get('product_id')
        users_product = Product.objects.get(id=users_product_id)
        return users_product

    def test_func(self):
        """ Ensures only the owner of the product can review it's offers"""
        if self.request.user == self.users_product.owner:
            return True
        return False


def review_single_offer(request, offered_product_id, users_product_id):
    """
    Review a single offer and process offer acceptance
    Parameters
    ----------
    request
    offered_product_id: int
        ID of product that user is reviewing
    users_product_id: int
        ID of product that user owns and that the offer has been made for
    """
    try:
        offered_product = Product.objects.get(id=offered_product_id)
        users_product = Product.objects.get(id=users_product_id)
    except:
        raise Http404('Oops - one of these products doesn\'t exist')

    if request.method == 'POST':
        """ accept offer """
        users_product.status = ProductStatus.PENDING_CHECKOUT
        users_product.save(update_fields=['status'])

        offered_product.status = ProductStatus.PENDING_CHECKOUT
        offered_product.save(update_fields=['status'])

        accepted_swap = Swap.objects.get(offered_product=offered_product, desired_product=users_product)
        accepted_swap.status = SwapStatus.PENDING_CHECKOUT
        accepted_swap.date_accepted = timezone.now()  # set match time
        accepted_swap.save(update_fields=['status', 'date_accepted'])

        # Reject other offers
        rejected_swaps = Swap.objects.filter(desired_product=users_product).exclude(offered_product=offered_product)
        for rejected_swap in rejected_swaps:
            rejected_swap.status = SwapStatus.REJECTED
            rejected_swap.save(update_fields=['status'])

        return redirect('checkout', product_id=users_product.id)

    else:
        context = {'product': offered_product,  # NOTE - important that context name is 'product'
                   'users_product': users_product}
        return render(request, template_name="swaps/review_single_offer.html", context=context)






