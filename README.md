# Malaika E-commerce Shop

A simple Django e-commerce application with PayPal integration.

## Features

- Product catalog with categories
- SEO-friendly slugs for products and categories
- Shopping cart functionality
- PayPal payment integration
- Order management
- User authentication
- Bootstrap 5 UI

## Models

1. **Category** - Product categories with slugs
2. **Product** - Products with name, description, price, stock, images, and slugs
3. **Cart** - Shopping carts for users and guest sessions
4. **CartItem** - Items in the cart
5. **Order** - Customer orders with billing information
6. **OrderItem** - Items in an order

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

5. Access the application:
- Frontend: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/

## PayPal Integration Setup

1. Get your PayPal Client ID from https://developer.paypal.com/
2. Replace `YOUR_PAYPAL_CLIENT_ID` in `ecommerce/templates/ecommerce/checkout.html` with your actual Client ID
3. For testing, use PayPal Sandbox credentials

## Usage

1. **Admin Panel**: Add categories and products through the Django admin panel
2. **Shopping**: Browse products, add to cart
3. **Checkout**: Fill billing information and pay with PayPal
4. **Orders**: View order history (for logged-in users)

## Project Structure

```
malaika/
├── malaika/                  # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── ecommerce/                # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin configuration
│   └── templates/           # HTML templates
│       ├── base.html
│       └── ecommerce/
│           ├── home.html
│           ├── product_list.html
│           ├── product_detail.html
│           ├── category_detail.html
│           ├── cart.html
│           ├── checkout.html
│           ├── order_success.html
│           ├── order_history.html
│           └── order_detail.html
├── manage.py
└── requirements.txt
```

## Key URLs

- `/` - Home page
- `/products/` - All products
- `/product/<slug>/` - Product detail
- `/category/<slug>/` - Category products
- `/cart/` - Shopping cart
- `/checkout/` - Checkout page
- `/order-history/` - Order history (requires login)

## Notes

- This is a simple implementation suitable for learning purposes
- For production use, add proper security measures, SSL, and payment verification
- The PayPal integration uses the PayPal JavaScript SDK
- Bootstrap 5 is used for styling (loaded from CDN)