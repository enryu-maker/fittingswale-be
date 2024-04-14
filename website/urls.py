from django.urls import path
from .views import BestSellerProductList, SpotlightProductList

urlpatterns = [
    path('bestsellers/', BestSellerProductList.as_view(), name='bestsellers-list'),
    path('spotlights/', SpotlightProductList.as_view(), name='spotlights-list'),
]
