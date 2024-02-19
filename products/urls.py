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
    path('',include(router.urls))
]
