from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.utils.encoding import smart_str
from rest_framework.viewsets import ModelViewSet
from products.models import Role,PaymentTransaction,SizeChart
import random
import string

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
    
def generate_password(length=12):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        try:
            user = User.objects.filter(email=request.data['email']).first()
        except:
            return Response({"msg":"No Email Provided"})
        if user:
            return Response({"msg":"User is already Registered"})

        if serializer.is_valid():
            user = serializer.save()
            otp = random.randint(1000, 9999)
            user.otp = otp
            user.save()
            send_mail(
                'Verification Code',
                f'Your verification code is {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email,is_trusty=False)
            if user.otp == int(otp):
                user.is_trusty = True
                user.otp=None
                user.save()
                return Response({'msg': 'Email verified successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'msg': 'User not found or already Verified'}, status=status.HTTP_404_NOT_FOUND)
        

class LoginUserAPIView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
        except:
            return Response({"msg":"Fields are empty"})
        user = authenticate(email=email, password=password)
        if user and user.is_trusty:
            tokens = get_tokens_for_user(user)
            role_id = Role.objects.get(title=user.role).id
            tokens['user_role'] = role_id
            tokens['is_profile_complete']= user.is_profile_complete()
            
            if user.is_verify or role_id == 1:
                tokens['is_verify'] = True
            else:
                tokens['is_verify'] = False
            
            return Response(tokens)
        return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class GoogleLoginAPIView(APIView):
    def post(self,request):
        try:
            email = request.data.get('email')
            user = User.objects.filter(email=email).first()
            if user is not None:
                tokens = get_tokens_for_user(user)
                return Response(tokens)
            name = request.data.get('name')
            password = generate_password()
            user = User(email=email,name=name,password=password)
            user.save()
            tokens = get_tokens_for_user(user)
            return Response(tokens)
        except:
            return Response({'msg':'An Error Occured'})

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        domain = request.data.get('domain')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_link = f"{domain}/reset-password/{uid}/{token}/"
        
        send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {reset_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        return Response({'msg': 'Password reset link sent successfully','link':reset_link}, status=status.HTTP_200_OK)

class ResetPasswordAPIView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            if new_password is None:
                return Response({"msg":"Please enter New PassWord"})
            user.set_password(new_password)
            user.save()
            return Response({'msg': 'Password reset successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Invalid password reset link'}, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    authentication_class = [JWTAuthentication,]
    def get(self,request):
        user = request.user
        try:
            print(user.email)
        except Exception as e:
            return Response({"msg":"AnonymousUser Cannot View Profile"})
        
        serializer = UserSerializer(user)
        data = serializer.data
        data['is_verified'] = True if (user.role=="Customer" or user.is_verify) else False
        return Response(data)


class EditUserAPIView(APIView):
    authentication_classes = [JWTAuthentication,]
    def get(self, request):
        user = request.user 
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserAddressAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        addresses = Address.objects.filter(user=user)
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        request.data['user'] = user.id

        Address.objects.filter(user=user).update(active=False)

        serializer = UserAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(active=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = request.user
        try:
            address = Address.objects.get(id=pk, user=user)
            serializer = UserAddressSerializer(address, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response({'msg': 'Address not found or does not belong to the authenticated user'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        user = request.user
        try:
            
            Address.objects.filter(user=user).update(active=False)
            
            address = Address.objects.get(id=pk, user=user)

            address.active = True
            address.save()

            return Response({'msg': 'Address updated successfully'}, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({'msg': 'Address not found or does not belong to the authenticated user'}, status=status.HTTP_404_NOT_FOUND)

    
    def delete(self, request, pk):
        user = request.user
        try:
            address = Address.objects.get(id=pk, user=user)
            
            if address.active:
                remaining_addresses = user.address_set.exclude(id=pk)
                if remaining_addresses.exists():
                    new_active_address = remaining_addresses.first()
                    new_active_address.active = True
                    new_active_address.save()
            
            address.delete() 
                
            return Response({'msg': 'Address deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response({'msg': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_list = []
        try:
            orders = PaymentTransaction.objects.filter(user=request.user)
        except:
            return Response({'msg':'No orders Found'})
        
        for order in orders:
            order_items = []
            for item in order.items:
                try:
                    product = Product.objects.get(id=item['product_id'])
                except:
                    size_chart = SizeChart.objects.get(id=item['product_id'])
                    product = size_chart.product
                size_chart = SizeChart.objects.get(id=item['size_id'])
                order_items.append({
                    "product": {
                        "id": product.id,
                        "product_name": product.product_name,
                    },
                    "size_chart": {
                        "id": size_chart.id,
                        "size":size_chart.size
                    },
                    "quantity": item['quantity']
                })
            
            order_dict = {
                "transaction_id": order.transaction_id,
                "payment_method": order.payment_method,
                "status": order.status,
                "payment_date": order.payment_date,
                "items": order_items,
                "address": order.address,
                "contact_details": order.contact_details,
                "total": order.total
            }
            order_list.append(order_dict)
        
        return Response({"orders": order_list})