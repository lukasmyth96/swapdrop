from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from .models import Like
from products.models import Product, ProductStatus
from matches.models import Offer, OfferStatus


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
        selected_product_ids = [int(_id) for _id in request.POST.getlist('image-picker-select')]

        # Show warning if no items have been offered
        if not selected_product_ids:
            messages.warning(request, 'You must select at least one item to offer')
            return redirect('make-offer', product_id=product_id)

        # Construct objects for offered products and desired product
        offered_products = [Product.objects.get(pk=product_id) for product_id in selected_product_ids]
        desired_product = Product.objects.get(pk=product_id)

        # Create and save offer objects
        for offered_product in offered_products:
            _offer, created_new = Offer.objects.get_or_create(offered_product=offered_product, desired_product=desired_product)
            if created_new:
                _offer.save()

        messages.success(request, 'Your offer has been sent')
        return redirect('product-feed')


    def get_queryset(self):
        """ Returns all products owned by currently logged in user"""
        all_products = super().get_queryset()
        users_products = all_products.filter(owner=self.request.user)
        return users_products


class ReviewOffersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Offer
    template_name = 'matches/review_offers.html'
    context_object_name = 'products'
    ordering = ['-date_posted']


    def get_queryset(self):
        """ Returns list of all products that have been offered for current product"""
        current_product = self.get_current_product()  # product that the offers are being made for

        if current_product.status == ProductStatus.LIVE:
            offers_for_product = self.get_offers_for_product(current_product=current_product)
            offered_products = [offer.offered_product for offer in offers_for_product]
        else:
            offered_products = []
            messages.warning(self.request, 'You have already accepted an offer on this product')

        return offered_products

    def post(self, request, product_id):
        """ Process acceptance of offer"""

        # Extract ids of selected products from the select box in the form
        # Note - by default a hidden <option> is selected on load with value=""
        assert len(request.POST.getlist('image-picker-select')) == 1
        selected_product_id = [_id for _id in request.POST.getlist('image-picker-select')][0]

        # Show warning if no items have been offered
        if not selected_product_id:
            messages.warning(request, 'You must select which offer to accept')
            return redirect('review-offers', product_id=product_id)

        # Update status of current product to MATCHED
        current_product = self.get_current_product(product_id=product_id)  # Product object
        assert current_product.status == ProductStatus.LIVE
        current_product.status = ProductStatus.MATCHED
        current_product.save(update_fields=['status'])

        # Update status of each offer and update the status of accepted product to MATCHED
        selected_product_id = int(selected_product_id)
        offers_for_product = self.get_offers_for_product(current_product=current_product)  # get list of offered products
        for offer in offers_for_product:
            offered_product = offer.offered_product
            if offered_product.id == selected_product_id:
                offer.status = OfferStatus.ACCEPTED  # update status of offer
                offered_product.status = ProductStatus.MATCHED  # update status of accepted product
                offered_product.save(update_fields=['status'])
            else:
                offer.status = OfferStatus.REJECTED
            offer.save(update_fields=['status'])  # update status in db

        messages.success(request, 'Congrats - match complete!')
        return redirect('profile')

    def test_func(self):
        """ Ensures only the owner of the product can review it's offers"""
        current_product = self.get_current_product()
        if self.request.user == current_product.owner:
            return True
        return False

    def get_current_product(self, product_id=None):
        if product_id is None:
            product_id = self.kwargs.get('product_id')  # for get requests
        current_product = Product.objects.get(id=product_id)
        return current_product

    @staticmethod
    def get_offers_for_product(current_product):
        """ Returns QuerySet of all offers for this product """
        offers_for_this_product = Offer.objects.filter(desired_product=current_product, status=OfferStatus.PENDING)
        return offers_for_this_product







