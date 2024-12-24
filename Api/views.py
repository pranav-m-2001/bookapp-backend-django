from django.shortcuts import render
from rest_framework.decorators import api_view,APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterCustomUserSerializer, UserRegisterSerializer,BookSerializer,OrderSerializer,UserProfileSerializer
from .models import UserProfile,CustomUser,Book,Order
from rest_framework.permissions import BasePermission,IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from allauth.socialaccount.models import SocialToken, SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import stripe


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

class AdminTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if not user.is_superuser:
            raise AuthenticationFailed('Only Admin can login')
        
        token = serializer.validated_data['access']
        refresh = serializer.validated_data['refresh']
        return Response({'access':str(token), 'refresh':str(refresh)})
    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CreateListBooksAdminView(APIView):

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request:Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request:Request, *args, **kwargs):
        books = Book.objects.all()
        serializer = self.serializer_class(books, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RetrieveDeleteBooks(APIView):

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request:Request, *args, **kwargs):
        book = Book.objects.get(id=request.data.get('bookId'))
        serializer = self.serializer_class(book, many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request:Request, *args, **kwargs):
        print(request.data.get('bookId'))
        book = Book.objects.get(id=request.data.get('bookId'))
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateBooks(APIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated,IsAdmin]

    def post(self, request:Request, *args, **kwargs):
        bookId = request.data.get('bookId')
        book = Book.objects.get(id=bookId)
        serializer = self.serializer_class(instance=book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Book Updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AllOrders(APIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request:Request, *args, **kwargs):
        order = Order.objects.all()
        serializer = self.serializer_class(order, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangeOrderStatus(APIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request:Request, *args, **kwargs):
        orderId = request.data.get('orderId')
        orderStatus = request.data.get('status')
        order = Order.objects.get(id=orderId)
        order.status = orderStatus
        order.save()
        return Response({'message':'Order Status Updated'},status=status.HTTP_200_OK)

        
    
    

    


# User Section

class CustomerTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if not user.is_customer:
            raise AuthenticationFailed('Only Customer can login')
        
        token = serializer.validated_data['access']
        refresh = serializer.validated_data['refresh']
        return Response({'access':str(token), 'refresh':str(refresh)})

class CreateUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request:Request, *args, **kwargs):
        username = request.data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            return Response({'message':'Username Alredy Exists'}, status=status.HTTP_208_ALREADY_REPORTED)
        serializer = RegisterCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_customer=True)
            user.set_password(serializer.validated_data['password'])
            user.save()
            user_profile = UserProfile.objects.create(user=user, name=serializer.validated_data['username'])
            user_profile.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
def login_googole_callback(request:Request):
    user = request.user
    social_accounts = SocialAccount.objects.filter(user=user)
    social_account = social_accounts.first()

    if not social_account:
        return Response({'message':'Account Not Found'}, status=status.HTTP_204_NO_CONTENT)

    token = SocialToken.objects.filter(account=social_account, account__provider='google').first()

    if token:
        refresh = RefreshToken.for_user(user=user)
        access_token = str(refresh.access_token)
        return Response({'access':access_token}, status=status.HTTP_200_OK)
    else:
        return Response({'message':'No token found'}, status=status.HTTP_204_NO_CONTENT)




class AllBooksView(APIView):
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get(self, request:Request, *args, **kwargs):
        books = Book.objects.all()
        serilaizer = self.serializer_class(books, many=True, context={'request':request})
        return Response(serilaizer.data, status=status.HTTP_200_OK)
    
class GetUserData(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request:Request, *args, **kwargs):
        userData = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(userData, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddToWishlist(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request:Request, *args, **kwargs):
        bookId = request.data.get('bookId')
        userData = UserProfile.objects.get(user=request.user)
        if bookId not in userData.wishlist:
            userData.wishlist.append(bookId)
            userData.save()
            return Response({'message':'Added to Wishlist'}, status=status.HTTP_200_OK)
        else:
            userData.wishlist.remove(bookId)
            userData.save()
            return Response({'message':'Book removed from Wishlist'}, status=status.HTTP_200_OK)


    
class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request:Request, *args, **kwargs):
        userData = UserProfile.objects.get(user=request.user)
        itemId = request.data.get('itemId')
        print(userData.cartdata)
        if userData.cartdata.get(str(itemId)):
            userData.cartdata[str(itemId)] += 1
        else:
            userData.cartdata[itemId] = 1
        userData.save()
        return Response({'message': 'Added To Cart'}, status=status.HTTP_200_OK)
    
class UpdateCart(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request:Request, *args, **kwargs):
        userData = UserProfile.objects.get(user=request.user)
        itemId = request.data.get('itemId')
        quantity = request.data.get('quantity')
        userData.cartdata[str(itemId)] = quantity
        userData.save()
        return Response({'message': 'Cart updated'}, status=status.HTTP_200_OK)


class CreateOrder(APIView):

    permission_classes = [IsAuthenticated]

    def post(slef, request:Request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            userData = UserProfile.objects.get(user=request.user)
            userData.cartdata = {}
            userData.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateOrderStripe(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request:Request, *args, **kwargs):
        try:
            serializer = OrderSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                order = serializer.save()
                line_items = []

                for item in request.data.get('items'):
                    line_items.append({
                        'price_data':{
                            'currency': 'inr',
                            'product_data':{
                                'name':item['name'],
                            },
                            'unit_amount':int(float(item['price']) * 100),
                        },
                        'quantity':item['quantity']
                    })

                line_items.append({
                    'price_data':{
                        'currency': 'inr',
                        'product_data':{
                            'name':'Delivery Charges',
                        },
                        'unit_amount':int(40 * 100),
                        },
                    'quantity':1
                })

                session = stripe.checkout.Session.create(
                    success_url= f'{settings.REACT_URL}/verify?success=true&orderId={order.pk}',
                    cancel_url=f'{settings.REACT_URL}/verify?success=false&orderId={order.pk}',
                    line_items=line_items,
                    mode='payment',
                )
                return Response({'message':'Order Created', 'session_url': session.url}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyStripePayment(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request:Request, *args, **kwargs):
        success = request.data.get('success')
        orderId = request.data.get('orderId')
        order = Order.objects.get(id=orderId)
        if success == 'true' or success:   
            order.payment = True
            order.save()
            userData = UserProfile.objects.get(user=request.user)
            userData.cartdata = {}
            userData.save()
            return Response({'success':True, 'message':'Order Place'}, status=status.HTTP_200_OK)
        else:
            order.payment = False
            order.save()
            return Response({'success':False, 'message':'Error Occured'}, status=status.HTTP_204_NO_CONTENT)



class GetUserOrder(APIView):

    serializer_class = OrderSerializer

    def get(self, request:Request, *args, **kwargs):
        order = Order.objects.filter(user=request.user.profile).exclude(paymentMethod='STRIPE', payment=False)
        serializer = OrderSerializer(order, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserProfile(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request:Request, *args, **kwargs):
        userData = UserProfile.objects.get(user=request.user)
        serializer = self.serializer_class(instance=userData, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Pofile updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


