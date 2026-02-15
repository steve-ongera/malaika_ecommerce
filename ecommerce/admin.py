# admin.py - Enhanced admin for payment management
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, Order, OrderItem, PaymentTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created_at']
    list_filter = ['available', 'category', 'created_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'full_name', 
        'email', 
        'phone',
        'total_amount',
        'payment_method_badge',
        'status_badge',
        'created_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at', 'paid_at']
    search_fields = ['id', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'paid_at',
        'paypal_order_id',
        'mpesa_checkout_request_id',
        'mpesa_transaction_id',
        'stripe_payment_intent_id'
    ]
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Information', {
            'fields': ('address', 'city', 'postal_code', 'country')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'currency', 'status', 'payment_method')
        }),
        ('Payment Gateway References', {
            'fields': (
                'paypal_order_id',
                'mpesa_checkout_request_id',
                'mpesa_transaction_id',
                'stripe_payment_intent_id'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Customer'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ff9800',
            'processing': '#2196f3',
            'paid': '#4caf50',
            'shipped': '#9c27b0',
            'delivered': '#00bcd4',
            'cancelled': '#f44336',
            'failed': '#e91e63'
        }
        color = colors.get(obj.status, '#757575')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def payment_method_badge(self, obj):
        icons = {
            'paypal': '💳',
            'mpesa': '📱',
            'card': '💳'
        }
        colors = {
            'paypal': '#0070ba',
            'mpesa': '#00a65a',
            'card': '#635bff'
        }
        icon = icons.get(obj.payment_method, '💰')
        color = colors.get(obj.payment_method, '#757575')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{} {}</span>',
            color,
            icon,
            obj.get_payment_method_display()
        )
    payment_method_badge.short_description = 'Payment Method'
    
    actions = ['mark_as_paid', 'mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_paid(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='paid', paid_at=timezone.now())
        self.message_user(request, f'{updated} order(s) marked as paid.')
    mark_as_paid.short_description = 'Mark selected orders as paid'
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} order(s) marked as shipped.')
    mark_as_shipped.short_description = 'Mark selected orders as shipped'
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_as_delivered.short_description = 'Mark selected orders as delivered'


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id',
        'order',
        'payment_method',
        'amount',
        'currency',
        'status_badge',
        'created_at'
    ]
    list_filter = ['payment_method', 'status', 'currency', 'created_at']
    search_fields = ['transaction_id', 'order__id', 'order__email']
    readonly_fields = ['created_at', 'updated_at', 'response_data']
    fieldsets = (
        ('Transaction Details', {
            'fields': ('order', 'payment_method', 'transaction_id')
        }),
        ('Amount', {
            'fields': ('amount', 'currency')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Response Data', {
            'fields': ('response_data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
    
    def status_badge(self, obj):
        colors = {
            'initiated': '#ff9800',
            'pending': '#2196f3',
            'completed': '#4caf50',
            'failed': '#f44336',
            'cancelled': '#757575'
        }
        color = colors.get(obj.status, '#757575')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'items_count', 'total', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_key']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items'
    
    def total(self, obj):
        return f"${obj.get_total()}"
    total.short_description = 'Total'