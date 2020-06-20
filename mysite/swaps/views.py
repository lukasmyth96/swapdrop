from django.shortcuts import redirect, render
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

    # def post(self, request, product_id):
    #     """ Process acceptance of offer"""
    #
    #     selected_product_id_str = request.POST.get('product_id')
    #     if selected_product_id_str is None:
    #         # Show warning if no items have been offered
    #         messages.warning(request, 'You must select one offer to accept')
    #         return redirect('review-offers', product_id=product_id)
    #
    #     selected_product_id = int(selected_product_id_str)  # cast to int
    #
    #     # Update status of current product to PENDING_CHECKOUT
    #     current_product = self.get_current_product(product_id=product_id)  # Product object
    #     assert current_product.status == ProductStatus.LIVE
    #     current_product.status = ProductStatus.PENDING_CHECKOUT
    #     current_product.save(update_fields=['status'])
    #
    #     # Update status of each offer and update the status of accepted product to PENDING_CHECKOUT
    #     offers_for_product = self.get_offers_for_product(current_product=current_product)  # get list of swaps that are offers for this product
    #     for offer in offers_for_product:
    #         offered_product = offer.offered_product
    #         if offered_product.id == selected_product_id:
    #             offer.status = SwapStatus.PENDING_CHECKOUT  # update status of swap
    #             offer.date_accepted = timezone.now()  # set match time
    #             offered_product.status = ProductStatus.PENDING_CHECKOUT  # update status of accepted product
    #             offered_product.save(update_fields=['status'])
    #         else:
    #             offer.status = SwapStatus.REJECTED
    #
    #         offer.save(update_fields=['status', 'date_accepted'])  # update status in db
    #
    #     return redirect('checkout', product_id=current_product.id)

    # def get_current_product(self, product_id=None):
    #     if product_id is None:
    #         product_id = self.kwargs.get('product_id')  # for get requests
    #     current_product = Product.objects.get(id=product_id)
    #     return current_product
    #
    # @staticmethod
    # def get_offers_for_product(current_product):
    #     """ Returns QuerySet of all offers for this product """
    #     offers_for_this_product = Swap.objects.filter(desired_product=current_product, status=SwapStatus.PENDING_REVIEW)
    #     return offers_for_this_product


def review_single_offer(request, offered_product_id, users_product_id):
    """
    Review a single offer
    Parameters
    ----------
    request
    offered_product_id: int
        ID of product that user is reviewing
    users_product_id: int
        ID of product that user owns and that the offer has been made for
    """
    offered_product = Product.objects.get(id=offered_product_id)
    users_product = Product.objects.get(id=users_product_id)

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






