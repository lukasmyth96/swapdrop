from django.urls import path

from .views import MakeOfferListView, ReviewOffersListView

urlpatterns = [
    path('make_offer/<int:product_id>/', MakeOfferListView.as_view(), name='make-offer'),
    path('review_offers/<int:product_id>/', ReviewOffersListView.as_view(), name='review-offers'),
]
