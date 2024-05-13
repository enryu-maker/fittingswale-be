from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.razor_pay.main import create_order,verify_payment_signature
from .serializers import RazorpayOrderSerializer,RazorpayTransactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from products.models import PaymentTransaction


class RazorpayOrderAPIView(APIView):
    
    def post(self, request):
        razorpay_order_serializer = RazorpayOrderSerializer(
            data=request.data
        )
        if razorpay_order_serializer.is_valid():
            order_response = create_order(
                amount=razorpay_order_serializer.validated_data.get("amount"),
                currency=razorpay_order_serializer.validated_data.get("currency")
            )
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order_response
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": razorpay_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class TransactionAPIView(APIView):
    authentication_class = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,] 
    def post(self, request):
        data = request.data
        order = PaymentTransaction.objects.get(pk=request.data.get('order_id'))
        transaction_serializer = RazorpayTransactionSerializer(data=data)
        if transaction_serializer.is_valid():
            # print(transaction_serializer.validated_data.get("razorpay_payment_id"))
            verify_payment_signature(
                razorpay_payment_id = transaction_serializer.validated_data.get("razorpay_payment_id"),
                razorpay_order_id = transaction_serializer.validated_data.get("razorpay_order_id"),
                razorpay_signature = transaction_serializer.validated_data.get("razorpay_signature")
            )
            # transaction_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "transaction created"
            }
            order.razorpay_order_id = transaction_serializer.validated_data.get("razorpay_payment_id")
            order.razorpay_order_id = transaction_serializer.validated_data.get("razorpay_order_id")
            order.razorpay_signature = transaction_serializer.validated_data.get("razorpay_signature")
            order.status = 'completed'
            
            order.save()
            
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": transaction_serializer.errors
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)