from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.payu.main import generate_payment_hash
from .serializers import PayUOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json


class PayUOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        payu_order_serializer = PayUOrderSerializer(
            data=request.data
        )
        if payu_order_serializer.is_valid():
            order_response = generate_payment_hash(
                amount=str(payu_order_serializer.validated_data.get("amount")),
                firstname=request.user.name,
                phonenumber=request.user.mobile_no,
                email=request.user.email,
                productinfo=json.dumps(
                    payu_order_serializer.validated_data.get("productinfo")),
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
                "error": payu_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
