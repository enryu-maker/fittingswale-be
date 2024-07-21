from django.urls import path
from .views import BestSellerProductList, SpotlightProductList, NewProductAPIView, RandomProductAPIView

urlpatterns = [
    path('bestsellers/', BestSellerProductList.as_view(), name='bestsellers-list'),
    path('spotlights/', SpotlightProductList.as_view(), name='spotlights-list'),
    path('new/', NewProductAPIView.as_view(), name="new-products"),
    path('random-products/', RandomProductAPIView.as_view(), name="random-products"),
]
