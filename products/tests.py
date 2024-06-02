from django.test import TestCase
from .models import SizeChart,Product,PaymentTransaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render

# Create your tests here.

# size_charts = SizeChart.objects.filter(id__in=size_ids).select_related('product')
class GetProductFromListAPIView(APIView):
    def get(self,request):
        product_list = [
            {"size_id": 262, "quantity": 3, "product_id": 262}, 
            {"size_id": 259, "quantity": 1, "product_id": 259}
        ]
        size_ids = [x["size_id"] for x in product_list]
        size_charts = SizeChart.objects.get(id=262)
        print(size_charts.product)
        print(size_charts)
        return Response({'yo':'yo'})
    
def product_list(request,order_id):
    order = PaymentTransaction.objects.get(pk=order_id)
    order_list = order.items
    size_chart_ids = [x['size_id'] for x in order_list]
    quantity = [x['quantity'] for x in order_list] 
    '''
    eg
    [
            {"size_id": 262, "quantity": 3, "product_id": 262}, 
            {"size_id": 259, "quantity": 1, "product_id": 259}
        ]
    '''
    size_chart_data = SizeChart.objects.filter(id__in=size_chart_ids)
    size_chart_data_with_quantity = [
        {'item': size_chart, 'quantity': qty}
        for size_chart, qty in zip(size_chart_data, quantity)
    ]
    print(size_chart_data_with_quantity[0]['item'].id)
    context = {
        'size_chart_data': size_chart_data_with_quantity
    }

    return render(request,'order_list.html',context)