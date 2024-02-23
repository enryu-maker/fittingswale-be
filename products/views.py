from rest_framework import viewsets
from .models import *
from .serializers import *
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})

class ProductDetailView(View):
    def get(self, request, pk):
        # Get the product with the specified primary key
        product = get_object_or_404(Product, pk=pk)
        sub_category = SubCategory.objects.all()
        main_category = MainCategory.objects.all()
        # Retrieve related objects for the product
        product_image = ProductImage.objects.filter(product=product)
        product_image_with_finish = MultiImages.objects.filter(prod_img__in=product_image)
        product_detail = ProductDetail.objects.filter(product=product)
        size_chart = SizeChart.objects.filter(product=product)
        prices_with_size_chart = RolePrice.objects.filter(size__in=size_chart)
        location = Location.objects.filter(product=product)
        # print()
        
        # Render the template with the retrieved data
        return render(request, 'product_detail.html', {
            'sub_categories':sub_category,
            'main_categories':main_category,
            'product': product,
            'product_image':product_image,
            'product_image_with_finish': product_image_with_finish,
            'product_detail': product_detail,
            'size_chart': size_chart,
            'prices_with_size_chart': prices_with_size_chart,
            'location': location,
        })
        
class AddImagesAndFinishesView(View):
    def get(self, request,pk):
        existing_finishes = Finish.objects.all()
        product = Product.objects.get(pk=pk)
        return render(request, 'add_images_and_finishes.html', {
            'product':product,
            'finishes': existing_finishes,
        })
    
    def post(self, request,pk):
        existing_finishes = Finish.objects.all()
        product = Product.objects.get(pk=pk)
        finish_id = request.POST.get('finish')
        finish = Finish.objects.get(pk=finish_id)
        image_files = request.FILES.getlist('image')
        try:
            product_image = ProductImage.objects.get(product=product,finish=finish)
            if product_image is None:
                product_image = ProductImage.objects.create(product=product, finish=finish)
        except:
            product_image = ProductImage.objects.create(product=product, finish=finish)
            
        for image_file in image_files:
            MultiImages.objects.create(image=image_file, prod_img=product_image)
        
        return redirect('add_images_and_finishes', pk=pk)
    
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

class MainCategoryWithSubcategoryApiView(APIView):
    def get(self, request, format=None):
        main_categories = MainCategory.objects.all()
        serializer = MainCategoryWithSubCategorySerializer(main_categories, many=True)
        return Response(serializer.data)

class SubCategoryWithProductApiView(APIView):
    def get(self, request,id,format=None):
        sub_category = SubCategory.objects.filter(pk=id)
        serializer = SubCategoryWithProductSerializer(sub_category, many=True)
        return Response(serializer.data)