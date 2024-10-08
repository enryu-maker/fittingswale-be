from dotenv import load_dotenv
import os
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from .models import *
from .serializers import *
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from django.forms import inlineformset_factory
from .forms import ProductForm, ProductImageForm, MultiImageForm
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.razor_pay.main import create_order
from accounts.payu.main import verify_payment


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        sub_category = SubCategory.objects.all()
        main_category = MainCategory.objects.all()
        product_image = ProductImage.objects.filter(product=product)
        product_image_with_finish = MultiImages.objects.filter(
            prod_img__in=product_image)
        product_detail = ProductDetail.objects.filter(product=product)
        size_chart = SizeChart.objects.filter(product=product)
        prices_with_size_chart = RolePrice.objects.filter(size__in=size_chart)
        location = Location.objects.filter(product=product)
        return render(request, 'product_detail.html', {
            'sub_categories': sub_category,
            'main_categories': main_category,
            'product': product,
            'product_image': product_image,
            'product_image_with_finish': product_image_with_finish,
            'product_detail': product_detail,
            'size_chart': size_chart,
            'prices_with_size_chart': prices_with_size_chart,
            'location': location,
        })


class AddImagesAndFinishesView(View):
    def get(self, request, pk):
        existing_finishes = Finish.objects.all()
        product = Product.objects.get(pk=pk)
        return render(request, 'add_images_and_finishes.html', {
            'product': product,
            'finishes': existing_finishes,
        })

    def post(self, request, pk):
        existing_finishes = Finish.objects.all()
        product = Product.objects.get(pk=pk)
        finish_id = request.POST.get('finish')
        finish = Finish.objects.get(pk=finish_id)
        image_files = request.FILES.getlist('image')
        try:
            product_image = ProductImage.objects.get(
                product=product, finish=finish)
            if product_image is None:
                product_image = ProductImage.objects.create(
                    product=product, finish=finish)
        except:
            product_image = ProductImage.objects.create(
                product=product, finish=finish)

        for image_file in image_files:
            MultiImages.objects.create(
                image=image_file, prod_img=product_image)

        return redirect('add_images_and_finishes', pk=pk)


class AddProductView(View):
    def get(self, request):
        return render(request, template_name="add_product_form.html")

    def post(self, request):
        if request.method == 'POST':
            forms_data = request.POST
            print(forms_data)
            return render(request, template_name='add_product_form.html')
        else:
            return JsonResponse({"error": "Invalid request method"}, status=400)


class MainCategoryViewSet(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryProductSerializer

    def get_serializer_context(self):
        role_id = 1
        if self.request.user.is_authenticated:
            if self.request.user.role == "Business":
                role_id = 3
            elif self.request.user.role == "Interior":
                role_id = 2
        context = super().get_serializer_context()
        context['role_id'] = role_id
        return context


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetriveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'id'


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class FinishViewSet(viewsets.ModelViewSet):
    queryset = Finish.objects.all()
    serializer_class = FinishSerializer


class ProductAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        role_id = 1
        if request.user.is_authenticated:
            if request.user.role == "Business":
                role_id = 3
            elif request.user.role == "Interior":
                role_id = 2
        try:
            product = Product.objects.get(pk=id)
            serializer = ProductSerializer(
                product, context={'role_id': role_id})
            return Response(serializer.data)
        except:
            return Response({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)


class SubCategoryWithProductApiView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, sub_id, format=None):
        role_id = 1
        if request.user.is_authenticated:
            if request.user.role == "Business":
                role_id = 3
            elif request.user.role == "Interior":
                role_id = 2

        sub_category = SubCategory.objects.filter(pk=sub_id)
        serializer = SubCategoryProductSerializer(
            sub_category, many=True, context={'role_id': role_id})
        return Response(serializer.data)


load_dotenv()
razor_pay_id = os.environ.get('RAZOR_PAY_ID')
secret = os.environ.get('SECRET_KEY')


class PaymentTransactionAPIView(APIView):
    authentication_class = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        if request.data['payment_method'] == 'online':
            try:
                order_response = create_order(
                    amount=request.data.get("total"),
                    currency="INR"
                )
                data = request.data
                data['user'] = request.user.id
                serializer = PaymentTransactionSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                response = {
                    "status_code": status.HTTP_201_CREATED,
                    "msg": "order created",
                    "order_id": serializer.data["id"],
                    "data": order_response,
                    "razor_pay_secrets": {"id": razor_pay_id, "secret": secret}
                }
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(response, status=status.HTTP_201_CREATED)
            except:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "msg": "bad request",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:

            data = request.data
            data['user'] = request.user.id
            serializer = PaymentTransactionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayUTransactionAPIView(APIView):
    authentication_class = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        if request.data['payment_method'] == 'online':
            try:
                data = request.data
                data['user'] = request.user.id
                serializer = PaymentTransactionSerializer(data=data)
                txnid = request.data["txnid"]

                if serializer.is_valid():
                    verResponse = verify_payment(
                        txnid=txnid)
                    print(txnid)
                    if verResponse == True:
                        print("hello")
                        serializer.save(status="success")
                        serializer.save(transaction_id=txnid)
                        response = {
                            "status_code": status.HTTP_201_CREATED,
                            "msg": "order created",
                            "order_id": serializer.data["id"],
                            "data": "order placed successfully",
                        }
                    else:
                        response = {
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "msg": "order not created",
                            "order_id": serializer.data["id"],
                            "data": "Verification Failed",
                        }
                        Response(response, status=status.HTTP_400_BAD_REQUEST)
                else:
                    response = {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "msg": "order created",
                        "order_id": serializer.data["id"],
                        "data": "data is incorrect",
                    }
                    return Response(response, status=status.HTTP_201_CREATED)

            except:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "msg": "bad request",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProductCreateView(View):
    def get(self, request):
        ProductImageFormSet = inlineformset_factory(
            Product, ProductImage, form=ProductImageForm, extra=1, can_delete=False, min_num=1, validate_min=True)
        form = ProductForm()
        formset = ProductImageFormSet()
        return render(request, 'product_form.html', {'form': form, 'formset': formset})

    def post(self, request):
        ProductImageFormSet = inlineformset_factory(
            Product, ProductImage, form=ProductImageForm, extra=1, can_delete=False, min_num=1, validate_min=True)
        MultiImageFormSet = inlineformset_factory(
            ProductImage, MultiImages, form=MultiImageForm, extra=1, can_delete=False, min_num=1, validate_min=True)
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.save()
            formset.instance = product
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
                multi_image_formset = MultiImageFormSet(
                    request.POST, request.FILES, instance=instance)
                if multi_image_formset.is_valid():
                    multi_image_formset.save()
            return redirect('success_url')
        return render(request, 'product_form.html', {'form': form, 'formset': formset})


class SearchResultsAPIView(APIView):
    authentication_classes = [JWTAuthentication,]

    def get(self, request):
        role_id = 1
        if request.user.is_authenticated:
            role_id = request.user.role.id if hasattr(
                request.user, 'role') else 1
        query = request.query_params.get("query")
        if query == '':
            return Response({'msg': 'Cannot Find Product'})
        products = Product.objects.filter(
            Q(product_name__search=query) | Q(description__search=query))
        return Response(ProductSerializer(products, many=True).data)
