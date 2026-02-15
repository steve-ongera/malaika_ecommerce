from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, Cart, CartItem, Order, OrderItem
import json
from django.db import models
from django.db.models import Q


def home(request):
    """Home page with featured products"""
    products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def product_list(request):
    """List all products"""
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'product_list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


def category_detail(request, slug):
    """Category page with products"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category_detail.html', context)


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    """View cart"""
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')


def update_cart(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('cart')


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


# views.py - Updated with multiple payment methods
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.conf import settings
from decimal import Decimal

from .models import Cart, CartItem, Order, OrderItem, Product, PaymentTransaction
from .paypal_service import PayPalService
from .mpesa_service import MPesaService


import logging
logger = logging.getLogger(__name__)


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def checkout(request):
    """Checkout page with multiple payment options"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    # Get PayPal client ID for frontend
    paypal_client_id = settings.PAYPAL_CLIENT_ID
    
    # Calculate totals
    subtotal = cart.get_total()
    shipping = Decimal('0.00')
    tax = Decimal('0.00')
    total = subtotal + shipping + tax
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'paypal_client_id': paypal_client_id,
        'paypal_mode': settings.PAYPAL_MODE,
        'enable_paypal': settings.ENABLE_PAYPAL,
        'enable_mpesa': settings.ENABLE_MPESA,
        'enable_card': settings.ENABLE_CARD_PAYMENT,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY if settings.ENABLE_CARD_PAYMENT else None,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    return render(request, 'checkout.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    """Create order after payment (handles all payment methods)"""
    try:
        data = json.loads(request.body)
        
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()
        
        if not cart_items:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        payment_method = data.get('payment_method', 'paypal')
        
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            postal_code=data.get('postal_code', ''),
            city=data.get('city', ''),
            country=data.get('country', 'KE'),
            payment_method=payment_method,
            total_amount=cart.get_total(),
            currency=data.get('currency', 'USD'),
            status='processing'
        )
        
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
        
        # Update payment-specific fields
        if payment_method == 'paypal':
            order.paypal_order_id = data.get('paypal_order_id', '')
            order.status = 'paid'
            order.paid_at = timezone.now()
            
            # Create transaction record
            PaymentTransaction.objects.create(
                order=order,
                payment_method='paypal',
                transaction_id=data.get('paypal_order_id', ''),
                amount=order.total_amount,
                currency=order.currency,
                status='completed',
                response_data=data.get('payment_details', {})
            )
            
        elif payment_method == 'mpesa':
            order.mpesa_checkout_request_id = data.get('checkout_request_id', '')
            # M-Pesa payment will be confirmed via callback
            
        elif payment_method == 'card':
            order.stripe_payment_intent_id = data.get('payment_intent_id', '')
            order.status = 'paid'
            order.paid_at = timezone.now()
        
        order.save()
        
        # Update stock if payment is confirmed
        if order.status == 'paid':
            for item in cart_items:
                item.product.stock -= item.quantity
                item.product.save()
            
            # Clear cart
            cart_items.delete()
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'status': order.status
        })
        
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def initiate_mpesa_payment(request):
    """Initiate M-Pesa STK push"""
    try:
        data = json.loads(request.body)
        
        phone_number = data.get('phone_number')
        amount = data.get('amount')
        order_id = data.get('order_id')
        
        if not all([phone_number, amount, order_id]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        mpesa_service = MPesaService()
        
        response = mpesa_service.stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=f"Order-{order_id}",
            transaction_desc=f"Payment for Order #{order_id}"
        )
        
        if response.get('ResponseCode') == '0':
            # Create transaction record
            order = Order.objects.get(id=order_id)
            PaymentTransaction.objects.create(
                order=order,
                payment_method='mpesa',
                transaction_id=response.get('CheckoutRequestID'),
                amount=Decimal(amount),
                currency='KES',
                status='pending',
                response_data=response
            )
            
            return JsonResponse({
                'success': True,
                'checkout_request_id': response.get('CheckoutRequestID'),
                'message': 'Payment request sent to your phone'
            })
        else:
            return JsonResponse({
                'error': response.get('ResponseDescription', 'Payment initiation failed')
            }, status=400)
            
    except Exception as e:
        logger.error(f"Error initiating M-Pesa payment: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def mpesa_callback(request):
    """Handle M-Pesa payment callback"""
    try:
        data = json.loads(request.body)
        
        result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        checkout_request_id = data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
        
        # Find transaction
        transaction = PaymentTransaction.objects.filter(
            transaction_id=checkout_request_id,
            payment_method='mpesa'
        ).first()
        
        if not transaction:
            logger.error(f"Transaction not found for CheckoutRequestID: {checkout_request_id}")
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Transaction not found'})
        
        order = transaction.order
        
        if result_code == 0:
            # Payment successful
            transaction.status = 'completed'
            transaction.response_data = data
            transaction.save()
            
            # Update order
            order.status = 'paid'
            order.paid_at = timezone.now()
            
            # Extract M-Pesa receipt number
            callback_metadata = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {})
            items = callback_metadata.get('Item', [])
            for item in items:
                if item.get('Name') == 'MpesaReceiptNumber':
                    order.mpesa_transaction_id = item.get('Value')
            
            order.save()
            
            # Update stock
            cart = Cart.objects.filter(
                models.Q(user=order.user) if order.user else models.Q(session_key=request.session.session_key)
            ).first()
            
            if cart:
                for item in cart.items.all():
                    item.product.stock -= item.quantity
                    item.product.save()
                cart.items.all().delete()
            
        else:
            # Payment failed
            transaction.status = 'failed'
            transaction.response_data = data
            transaction.save()
            
            order.status = 'failed'
            order.save()
        
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Success'})
        
    except Exception as e:
        logger.error(f"Error processing M-Pesa callback: {str(e)}")
        return JsonResponse({'ResultCode': 1, 'ResultDesc': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def create_stripe_payment_intent(request):
    """Create Stripe payment intent for card payments"""
    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        data = json.loads(request.body)
        amount = data.get('amount')
        currency = data.get('currency', 'usd')
        
        if not amount:
            return JsonResponse({'error': 'Amount is required'}, status=400)
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),  # Convert to cents
            currency=currency.lower(),
            metadata={'order_id': data.get('order_id')}
        )
        
        return JsonResponse({
            'success': True,
            'client_secret': intent.client_secret
        })
        
    except Exception as e:
        logger.error(f"Error creating Stripe payment intent: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'order_success.html', context)


def query_mpesa_status(request, checkout_request_id):
    """Query M-Pesa payment status"""
    try:
        mpesa_service = MPesaService()
        response = mpesa_service.query_stk_push(checkout_request_id)
        
        return JsonResponse({
            'success': True,
            'status': response
        })
        
    except Exception as e:
        logger.error(f"Error querying M-Pesa status: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def order_history(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'order_history.html', context)


@login_required
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'order_detail.html', context)