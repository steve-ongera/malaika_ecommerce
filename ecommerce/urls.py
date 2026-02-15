from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    # Checkout and order
    path('checkout/', views.checkout, name='checkout'),
    path('create-order/', views.create_order, name='create_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    
    # M-Pesa endpoints
    path('initiate-mpesa-payment/', views.initiate_mpesa_payment, name='initiate_mpesa_payment'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('query-mpesa-status/<str:checkout_request_id>/', views.query_mpesa_status, name='query_mpesa_status'),
    
    # Stripe endpoint
    path('create-stripe-payment-intent/', views.create_stripe_payment_intent, name='create_stripe_payment_intent'),
    path('create-order/', views.create_order, name='create_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]