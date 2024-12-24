from rest_framework import serializers
from .models import CustomUser,UserProfile,Book,Order


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'is_customer')
        extra_kwargs = {'password': {'write_only': True}}

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','name','dob','gender', 'phone', 'address1', 'address2', 'image', 'cartdata')

class BookSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Book
        fields = ('id','name', 'slug', 'description', 'category', 'image', 'price', 'popular')
    
    def get_image(self, obj):
        request = self.context.get('request')
        return request.get_absolute_uri(obj.image.url)

class OrderSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'user', 'items', 'amount', 'address', 'status', 'paymentMethod', 'payment', 'ordered_at')

    def create(self, validated_data):
        request = self.context.get('request')
        order = Order.objects.create(user=request.user.profile, **validated_data)
        order.save()
        return order

class UserProfileSerializer(serializers.ModelSerializer):
    user = RegisterCustomUserSerializer(read_only=True)
    image = serializers.ImageField()
    class Meta:
        model = UserProfile
        fields = ('id','user','name','dob','gender', 'phone', 'address1', 'address2', 'image', 'cartdata', 'wishlist')
    
    def get_image(self, obj):
        request = self.context.get('request')
        return request.get_absolute_uri(obj.image.url)
