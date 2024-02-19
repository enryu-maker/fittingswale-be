from rest_framework import viewsets
from .models import *
from .serializers import *

class MainCategoryViewSet(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    
class RoleViewSet(viewsets.ModelViewSet):
    queryset= Role.objects.all()
    serializer_class = RoleSerializer
    
class FinishViewSet(viewsets.ModelViewSet):
    queryset = Finish.objects.all()
    serializer_class = FinishSerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer