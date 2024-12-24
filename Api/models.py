from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils.crypto import get_random_string

# Create your models here.

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=155)
    phone = models.IntegerField(null=True)
    address1 = models.CharField(max_length=155)
    address2 = models.CharField(max_length=155)
    dob = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='customer/', null=True, blank=True)
    cartdata = models.JSONField(default=dict, null=True)
    wishlist = models.JSONField(default=list, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=155)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=155)
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    popular = models.BooleanField(default=False)

    def save(self,*args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            if Book.objects.filter(slug=slug).exists():
                slug = f'{slug}-{get_random_string(5)}'
            self.slug = slug
        super(Book,self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order')
    items = models.JSONField(default=list, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    address = models.JSONField(default=dict, null=True)
    status = models.CharField(max_length=100, default='Order placed')
    paymentMethod = models.CharField(max_length=100)
    payment = models.BooleanField(default=False)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username