from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'main-categories', MainCategoryViewSet,basename='main-categories')
router.register(r'sub-categories', SubCategoryViewSet,basename='sub-categories')
router.register(r'roles',RoleViewSet,basename='role')
router.register(r'finish',FinishViewSet,basename='finsh')
router.register(r'view',ProductViewSet,basename='view')

urlpatterns = [
    path('',include(router.urls)),
    path('main-category-with-sub/',MainCategoryWithSubcategoryApiView.as_view()),
    path('sub-category-with-prod/<int:id>/',SubCategoryWithProductApiView.as_view()),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-images-and-finishes/<int:pk>', AddImagesAndFinishesView.as_view(), name='add_images_and_finishes'),
]
