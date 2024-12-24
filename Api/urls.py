from django.urls import path
from . import views
urlpatterns = [
    # Admin Section
    path('admin/token/', views.AdminTokenObtainPairView.as_view(), name='admin'),
    path('create-list-book/', views.CreateListBooksAdminView.as_view(), name='create-list-book'),
    path('get-update-delete-book/', views.RetrieveDeleteBooks.as_view(), name='get-update-delete-book'),
    path('all-orders/', views.AllOrders.as_view(), name='all-orders'),
    path('change-order-status/', views.ChangeOrderStatus.as_view(), name='change-order-status'),
    path('update-book/', views.UpdateBooks.as_view(), name='update-book'),

    # User Section
    path('login-user/', views.CustomerTokenObtainPairView.as_view(), name='login-user'),
    path('register-user/', views.CreateUserView.as_view(), name='register-user'),
    path('all-books/', views.AllBooksView.as_view(), name='all-books'),
    path('wishlist/', views.AddToWishlist.as_view(), name='wishlist'),
    path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('update-cart/', views.UpdateCart.as_view(), name='update-cart'),
    path('get-user/', views.GetUserData.as_view(), name='get-user'),
    path('place-order/', views.CreateOrder.as_view(), name='place-order'),
    path('place-order-stripe/', views.CreateOrderStripe.as_view(), name='place-order-stripe'),
    path('verify-stripe-payment/', views.VerifyStripePayment.as_view(), name='verify-stripe-payment'),
    path('user-order/', views.GetUserOrder.as_view(), name='user-order'),
    path('update-user/', views.UpdateUserProfile.as_view(), name='update-user'),
]