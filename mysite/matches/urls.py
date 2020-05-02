from django.urls import path

from .views import like, make_offer

urlpatterns = [
    path('like/<int:product_id>/', like, name='product-like'),
    path('make_offer/<int:product_id>/', make_offer, name='product-make-offer')
]
