from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from .tests import GetProductFromListAPIView,product_list

router = DefaultRouter()
router.register(r'main-categories', MainCategoryViewSet,basename='main-categories')
router.register(r'categories', CategoryViewSet,basename='categories')
router.register(r'sub-categories', SubCategoryViewSet,basename='sub-categories')
router.register(r'roles',RoleViewSet,basename='role')
router.register(r'finish',FinishViewSet,basename='finsh')

urlpatterns = [
    path('',include(router.urls)),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('category/<int:id>/', CategoryRetriveAPIView.as_view(), name='category-view'),
    path('view/<int:id>/', ProductAPIView.as_view(), name='product-list'),
    path('sub-cat/<int:sub_id>/', SubCategoryWithProductApiView.as_view(), name='product-list'),
    path('add/', ProductCreateView.as_view(), name='add'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-images-and-finishes/<int:pk>', AddImagesAndFinishesView.as_view(), name='add-images-and-finishes'),
    path('search/',SearchResultsAPIView.as_view(), name='search-product'),
    path('test/',GetProductFromListAPIView.as_view(),name='yes'),
    path('test-product/<int:order_id>/',product_list,name='yes'),
]
