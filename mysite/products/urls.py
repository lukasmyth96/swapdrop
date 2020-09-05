from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
)


urlpatterns = [
    path('feed/', login_required(ProductListView.as_view()), name='product-feed'),
    path('product/<int:pk>/', login_required(ProductDetailView.as_view()), name='product-detail'),
    path('product/new/', login_required(ProductCreateView.as_view()), name='product-create'),
    path('product/<int:pk>/update/', login_required(ProductUpdateView.as_view()), name='product-update'),
    path('product/<int:pk>/delete/', login_required(ProductDeleteView.as_view()), name='product-delete')
]