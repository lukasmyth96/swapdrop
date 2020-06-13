from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import MakeOfferListView, ReviewOffersListView

urlpatterns = [
    path('make_offer/<int:product_id>/', login_required(MakeOfferListView.as_view()), name='make-offer'),
    path('review_offers/<int:product_id>/', login_required(ReviewOffersListView.as_view()), name='review-offers'),
]
