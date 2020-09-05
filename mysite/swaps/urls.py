from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import MakeOfferListView, cancel_offers, ReviewOffersListView, review_single_offer

urlpatterns = [
    path('make_offer/<int:product_id>/', login_required(MakeOfferListView.as_view()), name='make-offer'),
    path('cancel_offers/<int:product_id>', login_required(cancel_offers), name='cancel-offers'),
    path('review_offers/<int:product_id>/', login_required(ReviewOffersListView.as_view()), name='review-offers'),
    path('review_offer/<int:offered_product_id>/<int:users_product_id>/', review_single_offer, name='review-single-offer')
]
