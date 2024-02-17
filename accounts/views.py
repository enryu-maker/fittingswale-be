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

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
    

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
            return Response(tokens)
        return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_link = f"{settings.DOMAIN}/reset-password/{uid}/{token}/"
        
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
        return Response(serializer.data)


class EditUserAPIView(APIView):
    authentication_classes = [JWTAuthentication,]
    # permission_classes = ['']
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
    

# class UserAddressAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         addresses = Address.objects.filter(user=user)
#         serializer = UserAddressSerializer(addresses, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         user = request.user
#         request.data['user'] = user.id

#         Address.objects.filter(user=user).update(active=False)

#         serializer = UserAddressSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(active=True)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, pk):
#         user = request.user
#         try:
#             address = Address.objects.get(id=pk, user=user)
#             serializer = UserAddressSerializer(address, data=request.data, partial=True)

#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Address.DoesNotExist:
#             return Response({'msg': 'Address not found or does not belong to the authenticated user'}, status=status.HTTP_404_NOT_FOUND)
        
#     def put(self, request, pk):
#         user = request.user
#         try:
            
#             Address.objects.filter(user=user).update(active=False)
            
#             address = Address.objects.get(id=pk, user=user)

#             address.active = True
#             address.save()

#             return Response({'msg': 'Address updated successfully'}, status=status.HTTP_200_OK)
#         except Address.DoesNotExist:
#             return Response({'msg': 'Address not found or does not belong to the authenticated user'}, status=status.HTTP_404_NOT_FOUND)

    
#     def delete(self, request, pk):
#         user = request.user
#         try:
#             address = Address.objects.get(id=pk, user=user)
            
#             if address.active:
#                 # Find any other address for the user and set it as active
#                 remaining_addresses = user.address_set.exclude(id=pk)
#                 if remaining_addresses.exists():
#                     new_active_address = remaining_addresses.first()
#                     new_active_address.active = True
#                     new_active_address.save()
            
#             address.delete() 
                
#             return Response({'msg': 'Address deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#         except Address.DoesNotExist:
#             return Response({'msg': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
        

# class UserSettingsAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             settings = Settings.objects.get(user=user)
#             serializer = SettingsSerializer(settings)
#             return Response(serializer.data)
#         except Settings.DoesNotExist:
#             settings = Settings.objects.create(user=user)
#             serializer = SettingsSerializer(settings)
#             return Response(serializer.data)

#     def post(self, request):
#         user = request.user
#         serializer = SettingsSerializer(data=request.data)
#         if serializer.is_valid():
#             existing_settings = Settings.objects.filter(user=user)
#             if existing_settings.exists():
#                 existing_settings.update(**serializer.validated_data)
#             else:
#                 serializer.save(user=user)
#             return Response({"data":serializer.data,'msg': 'Settings updated successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class RatingAndReviewsAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         reviews = RatingAndReviews.objects.filter(user=user)
#         serializer = RatingAndReviewsSerializer(reviews, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         user = request.user
#         product_id = request.data.get('product')

#         # Check if a review already exists for the same product by the same user
#         existing_review = RatingAndReviews.objects.filter(user=user, product=product_id).first()

#         if existing_review:
#             return Response({'msg': 'Review already exists for this product by the same user'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = RatingAndReviewsSerializer(data=request.data, context={'request': request})

#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Review posted successfully'}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ShoppingCartAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         cart_items = ShoppingCart.objects.filter(user=user)
#         serializer = ShoppingCartSerializer(cart_items, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         user = request.user
#         product_id = request.data.get('product')
#         quantity = request.data.get('quantity', 1)  # Default to 1 if quantity is not provided

#         # Check if the product is already in the user's shopping cart
#         existing_item = ShoppingCart.objects.filter(user=user, product=product_id).first()

#         if existing_item:
#             # If the product is already in the cart, update the quantity
#             existing_item.quantity += int(quantity)
#             existing_item.save()
#             serializer = ShoppingCartSerializer(existing_item)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             # If the product is not in the cart, create a new entry
#             new_item = ShoppingCart(user=user, product_id=product_id, quantity=quantity)
#             new_item.save()
#             serializer = ShoppingCartSerializer(new_item)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
# class StarCoinsAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         star_coins = StarCoins.objects.get_or_create(user=user)[0]
#         serializer = StarCoinsSerializer(star_coins)
#         return Response(serializer.data)

#     def post(self, request):
#         user = request.user
#         serializer = StarCoinsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request):
#         user = request.user
#         star_coins = StarCoins.objects.get_or_create(user=user)[0]
#         serializer = StarCoinsSerializer(star_coins, data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request):
#         user = request.user
#         star_coins = StarCoins.objects.get_or_create(user=user)[0]
#         serializer = StarCoinsSerializer(star_coins, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save(user=user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class OrderHistoryAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         order_history = OrderHistory.objects.filter(user=user)
#         serializer = OrderHistorySerializer(order_history, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         user = request.user
#         try:
#             product=Product.objects.filter(pk=request.data['product']).first()
#             order_history = OrderHistory.objects.create(product=product,user=user)
#             order_history.save()
#             return Response({"msg":"history added"})
#         except:
#             return Response({"msg":"Internal Error Occur"})

    
class AllUsersAPIView(APIView):
    def get(self,request):
        user = MyUser.objects.all()
        serializer = MyUserSerializer(user,many=True)
        return Response(serializer.data)