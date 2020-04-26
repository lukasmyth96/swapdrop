from django.urls import path

from .views import like

urlpatterns = [
    path('like/<int:product_id>/', like, name='product-like')
]
