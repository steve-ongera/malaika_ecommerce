# 🛍️ Malaika E-commerce Platform

[![Django Version](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PayPal](https://img.shields.io/badge/PayPal-Integrated-003087.svg)](https://www.paypal.com/)
[![M-Pesa](https://img.shields.io/badge/M--Pesa-Integrated-00A65A.svg)](https://developer.safaricom.co.ke/)
[![Stripe](https://img.shields.io/badge/Stripe-Integrated-635BFF.svg)](https://stripe.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **production-ready**, **scalable** Django e-commerce platform with comprehensive multi-payment gateway integration, advanced features, and enterprise-grade architecture.

## 🌟 Key Features

### 💳 **Multi-Payment Gateway Integration**
- **PayPal** - Complete checkout flow with sandbox and production support
- **M-Pesa** - Safaricom Daraja API integration for mobile money (STK Push)
- **Stripe** - Credit/Debit card payments (Visa, Mastercard, Amex)
- Real-time payment verification and callbacks
- Comprehensive transaction logging and monitoring
- Automatic payment reconciliation

### 🛒 **Advanced E-commerce Features**
- Product catalog with unlimited categories and subcategories
- SEO-optimized product and category pages with custom slugs
- Advanced search and filtering capabilities
- Smart shopping cart with session persistence
- Guest checkout and registered user checkout
- Inventory management with low-stock alerts
- Order tracking and status updates
- Email notifications for orders and shipping

### 🔐 **Security & Performance**
- CSRF protection on all forms
- Secure payment processing (PCI DSS compliant via Stripe)
- Environment-based configuration (dev/staging/production)
- Rate limiting on payment endpoints
- SQL injection protection via Django ORM
- XSS protection
- Secure session management
- HTTPS enforcement in production

### 📊 **Admin & Management**
- Enhanced Django admin with visual dashboards
- Order management with status tracking
- Payment transaction monitoring
- Inventory tracking and alerts
- Customer management
- Sales analytics and reporting
- Bulk operations support
- Export orders to CSV/Excel

### 🎨 **Modern UI/UX**
- Responsive design (mobile-first)
- Bootstrap 5 framework
- Intuitive checkout process
- Real-time cart updates
- Payment method selection interface
- Order confirmation pages
- Interactive elements with animations

## 📋 Table of Contents

- [Features Overview](#-key-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Payment Integration](#-payment-integration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🏗️ Architecture

### Technology Stack

**Backend:**
- Django 4.2+ (Python Web Framework)
- Django ORM (Database Abstraction)
- Django REST Framework (API endpoints)
- Celery (Async tasks & scheduled jobs)
- Redis (Caching & message broker)

**Payment Gateways:**
- PayPal REST API v2
- Safaricom Daraja API (M-Pesa)
- Stripe Payment Intents API

**Frontend:**
- Bootstrap 5
- JavaScript (Vanilla & ES6+)
- PayPal JavaScript SDK
- Stripe.js

**Database:**
- PostgreSQL (Production)
- SQLite (Development)

**Infrastructure:**
- Nginx (Web server & reverse proxy)
- Gunicorn (WSGI server)
- Docker & Docker Compose (Containerization)
- AWS S3 (Media storage - optional)

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Load Balancer                         │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
┌───────────────▼──────────────┐ ┌─────────▼────────────────┐
│     Nginx (Web Server)        │ │    Nginx (Web Server)    │
└───────────────┬──────────────┘ └─────────┬────────────────┘
                │                           │
┌───────────────▼──────────────┐ ┌─────────▼────────────────┐
│   Gunicorn (App Server)       │ │  Gunicorn (App Server)   │
│   Django Application          │ │  Django Application      │
└───────────────┬──────────────┘ └─────────┬────────────────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                ┌─────────────▼─────────────┐
                │    PostgreSQL Database     │
                └────────────────────────────┘
                              │
                ┌─────────────▼─────────────┐
                │      Redis Cache           │
                └────────────────────────────┘
                              │
        ┌────────────────────┴────────────────────┐
        │                     │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│  PayPal API    │  │   M-Pesa API    │  │  Stripe API    │
└────────────────┘  └─────────────────┘  └────────────────┘
```

## 📦 Data Models

### Core Models

#### **Category**
```python
- name: CharField          # Category name
- slug: SlugField         # SEO-friendly URL slug
- description: TextField  # Category description
- parent: ForeignKey      # For subcategories (optional)
- image: ImageField       # Category image
- created_at: DateTimeField
```

#### **Product**
```python
- name: CharField              # Product name
- slug: SlugField             # SEO-friendly URL slug
- category: ForeignKey        # Product category
- description: TextField      # Product details
- price: DecimalField         # Product price
- stock: IntegerField         # Available quantity
- image: ImageField           # Product image
- available: BooleanField     # Visibility status
- featured: BooleanField      # Featured products
- sku: CharField              # Stock keeping unit
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### **Cart & CartItem**
```python
Cart:
- user: ForeignKey (nullable)        # Registered user
- session_key: CharField (nullable)  # Guest session
- created_at: DateTimeField
- updated_at: DateTimeField

CartItem:
- cart: ForeignKey           # Parent cart
- product: ForeignKey        # Product reference
- quantity: PositiveIntegerField
- added_at: DateTimeField
```

#### **Order**
```python
- order_number: CharField (auto-generated)
- user: ForeignKey (nullable)
- first_name: CharField
- last_name: CharField
- email: EmailField
- phone: CharField
- address: CharField
- city: CharField
- postal_code: CharField
- country: CharField
- payment_method: CharField (paypal/mpesa/card)
- status: CharField (pending/processing/paid/shipped/delivered/cancelled/failed)
- total_amount: DecimalField
- currency: CharField
- paypal_order_id: CharField (nullable)
- mpesa_checkout_request_id: CharField (nullable)
- mpesa_transaction_id: CharField (nullable)
- stripe_payment_intent_id: CharField (nullable)
- created_at: DateTimeField
- updated_at: DateTimeField
- paid_at: DateTimeField (nullable)
- shipped_at: DateTimeField (nullable)
- delivered_at: DateTimeField (nullable)
```

#### **OrderItem**
```python
- order: ForeignKey
- product: ForeignKey
- price: DecimalField        # Price at time of purchase
- quantity: PositiveIntegerField
- subtotal: DecimalField     # price × quantity
```

#### **PaymentTransaction**
```python
- order: ForeignKey
- payment_method: CharField
- transaction_id: CharField (unique)
- amount: DecimalField
- currency: CharField
- status: CharField (initiated/pending/completed/failed/cancelled)
- response_data: JSONField   # Raw API response
- created_at: DateTimeField
- updated_at: DateTimeField
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL 12+ (for production)
- Redis 6+ (for caching and Celery)
- Git

### Quick Start (Development)

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/malaika-shop.git
cd malaika-shop
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Load Sample Data (Optional)**
```bash
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/products.json
```

8. **Run Development Server**
```bash
python manage.py runserver
```

9. **Access the Application**
- Frontend: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/

### Automated Setup (Recommended)

```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Create virtual environment
- Install all dependencies
- Generate Django secret key
- Run database migrations
- Prompt for superuser creation
- Set up directory structure
- Collect static files

## ⚙️ Configuration

### Environment Variables (.env)

The application uses environment variables for configuration. All sensitive data should be stored in the `.env` file.

**Critical Settings:**
```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PayPal
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID_SANDBOX=your_sandbox_client_id
PAYPAL_CLIENT_SECRET_SANDBOX=your_sandbox_secret
PAYPAL_CLIENT_ID_LIVE=your_live_client_id
PAYPAL_CLIENT_SECRET_LIVE=your_live_secret

# M-Pesa
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/mpesa/callback/

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Database (Production)
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

**See `.env.example` for complete configuration options.**

### Django Settings

The project uses environment-based configuration:

- **Development**: `DEBUG=True`, SQLite database
- **Staging**: `DEBUG=False`, PostgreSQL, limited features
- **Production**: `DEBUG=False`, PostgreSQL, all security features enabled

## 💳 Payment Integration

### PayPal Setup

1. **Create PayPal Developer Account**
   - Visit: https://developer.paypal.com/
   - Sign up or log in

2. **Create Application**
   - Go to "My Apps & Credentials"
   - Click "Create App"
   - Select "Merchant" as app type
   - Save Client ID and Secret

3. **Configure Sandbox**
   - Create test buyer accounts
   - Fund test accounts with sandbox money
   - Test transactions in sandbox mode

4. **Configure Application**
```python
# Already configured in .env
PAYPAL_CLIENT_ID_SANDBOX=AQubh87uHUffwKGIfVHOl2jjWa0y9m4EQCt41SyLpxc83ATuZa2ayNExvaxIksFbXpJ7lMTfnwxwS6bO
PAYPAL_CLIENT_SECRET_SANDBOX=EJdwn2DaJZdtgPqCSBKkScjYTqHky8ZzzZMuNe3Oa9Tvu4f3gv8idX5Wr_dDX5QXiF6so6owTm2Jxxdm
```

### M-Pesa Setup

1. **Register on Daraja Portal**
   - Visit: https://developer.safaricom.co.ke/
   - Create account and verify

2. **Create Daraja Application**
   - Login to portal
   - Create new app
   - Select "Lipa Na M-Pesa Online"
   - Get Consumer Key and Secret

3. **Get Paybill & Passkey**
   - For sandbox: Use test credentials
   - For production: Contact Safaricom

4. **Setup Callback URL**
   ```bash
   # For local testing with ngrok
   ngrok http 8000
   # Use the HTTPS URL in .env
   ```

### Stripe Setup

1. **Create Stripe Account**
   - Visit: https://stripe.com/
   - Sign up for account

2. **Get API Keys**
   - Dashboard > Developers > API Keys
   - Copy Publishable and Secret keys

3. **Configure Webhooks**
   - Dashboard > Developers > Webhooks
   - Add endpoint: `https://yourdomain.com/stripe/webhook/`
   - Select events to monitor

### Payment Flow

```
Customer Initiates Checkout
         │
         ├──> Selects Payment Method
         │
    ┌────┴────┬────────────┬──────────┐
    │         │            │          │
PayPal    M-Pesa      Card (Stripe)  │
    │         │            │          │
    ├─> API   ├─> STK      ├─> Payment│
    │   Call  │   Push     │   Intent │
    │         │            │          │
    ├─> User  ├─> User     ├─> User   │
    │   Login │   Enters   │   Enters │
    │   &     │   PIN      │   Card   │
    │   Pay   │            │   Details│
    │         │            │          │
    ├─> Capture ├─> Callback ├─> Confirm│
    │         │   Verify   │   Payment│
    │         │            │          │
    └────┬────┴────────────┴──────────┘
         │
    Order Confirmed
         │
    Update Inventory
         │
    Send Email Notification
         │
    Display Success Page
```

## 📖 Usage

### Admin Panel

Access the admin panel at `/admin/` with superuser credentials.

**Key Functions:**
- **Dashboard**: Overview of orders, products, and sales
- **Products**: Add, edit, delete products
- **Categories**: Manage product categories
- **Orders**: View and manage orders
- **Transactions**: Monitor all payment transactions
- **Users**: Manage customer accounts

### Customer Flow

1. **Browse Products**
   - View all products at `/products/`
   - Filter by category
   - Search for products

2. **Product Details**
   - View detailed product information
   - Check availability
   - Add to cart

3. **Shopping Cart**
   - View cart at `/cart/`
   - Update quantities
   - Remove items
   - Proceed to checkout

4. **Checkout**
   - Fill billing information
   - Select payment method
   - Complete payment
   - Receive confirmation

5. **Order Tracking**
   - View order history (logged-in users)
   - Track order status
   - View order details

## 🔌 API Documentation

### Payment Endpoints

#### Create Order
```http
POST /create-order/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+254712345678",
  "address": "123 Main St",
  "city": "Nairobi",
  "postal_code": "00100",
  "payment_method": "paypal",
  "paypal_order_id": "ORDER_ID"
}
```

#### Initiate M-Pesa Payment
```http
POST /initiate-mpesa-payment/
Content-Type: application/json

{
  "phone_number": "254712345678",
  "amount": "1000",
  "order_id": "123"
}
```

#### M-Pesa Callback
```http
POST /mpesa/callback/
Content-Type: application/json

{
  "Body": {
    "stkCallback": {
      "ResultCode": 0,
      "CheckoutRequestID": "ws_CO_...",
      "CallbackMetadata": {...}
    }
  }
}
```

#### Create Stripe Payment Intent
```http
POST /create-stripe-payment-intent/
Content-Type: application/json

{
  "amount": "100.00",
  "currency": "usd",
  "order_id": "123"
}
```

## 🧪 Testing

### Unit Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test shop.tests.test_models

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Integration Tests

```bash
# Test payment flows
python manage.py test shop.tests.test_payments

# Test checkout process
python manage.py test shop.tests.test_checkout
```

### Manual Testing

**PayPal Sandbox Testing:**
1. Use test buyer accounts from PayPal Developer Dashboard
2. Complete checkout with test account
3. Verify order creation and status

**M-Pesa Sandbox Testing:**
1. Use test phone: `254708374149`
2. Enter any 4-digit PIN
3. Verify callback reception

**Stripe Testing:**
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- 3D Secure: `4000 0025 0000 3155`

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL database
- [ ] Enable HTTPS
- [ ] Set up static file serving (Nginx/S3)
- [ ] Configure email backend
- [ ] Set up error monitoring (Sentry)
- [ ] Enable payment gateway webhooks
- [ ] Set up automated backups
- [ ] Configure Redis for caching
- [ ] Set up Celery for async tasks
- [ ] Implement rate limiting
- [ ] Configure logging
- [ ] Run security audit

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Server Deployment (Ubuntu)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev nginx

# Clone repository
git clone https://github.com/yourusername/malaika-shop.git
cd malaika-shop

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install gunicorn

# Configure environment
cp .env.example .env
nano .env  # Edit with production values

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Set up Gunicorn systemd service
sudo nano /etc/systemd/system/malaika.service

# Configure Nginx
sudo nano /etc/nginx/sites-available/malaika

# Enable and start services
sudo systemctl enable malaika
sudo systemctl start malaika
sudo nginx -t
sudo systemctl restart nginx
```

## 🔧 Troubleshooting

### Common Issues

**Issue: PayPal button not showing**
```bash
Solution:
1. Check Client ID in .env
2. Verify PayPal SDK is loading
3. Check browser console for errors
4. Ensure HTTPS in production
```

**Issue: M-Pesa callback not received**
```bash
Solution:
1. Verify ngrok is running (local dev)
2. Check callback URL is accessible
3. Ensure URL uses HTTPS
4. Check firewall settings
5. Verify Consumer Key/Secret
```

**Issue: Stripe payment fails**
```bash
Solution:
1. Verify API keys are correct
2. Check test card numbers
3. Ensure Stripe.js is loaded
4. Check browser console
5. Verify payment amount format
```

**Issue: Database connection error**
```bash
Solution:
1. Check PostgreSQL is running
2. Verify database credentials
3. Ensure database exists
4. Check DB_HOST and DB_PORT
```

## 📁 Project Structure

```
malaika-shop/
├── malaika/                      # Project configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
├── shop/                         # Main application
│   ├── models.py                # Database models
│   ├── views.py                 # View functions
│   ├── urls.py                  # URL routing
│   ├── admin.py                 # Admin configuration
│   ├── forms.py                 # Form definitions
│   ├── signals.py               # Django signals
│   ├── paypal_service.py        # PayPal integration
│   ├── mpesa_service.py         # M-Pesa integration
│   ├── templates/               # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── category_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_success.html
│   │   ├── order_history.html
│   │   └── order_detail.html
│   ├── static/                  # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── tests/                   # Test suite
│       ├── test_models.py
│       ├── test_views.py
│       └── test_payments.py
├── media/                        # User uploads
│   └── products/
├── staticfiles/                  # Collected static files
├── logs/                         # Application logs
├── fixtures/                     # Sample data
│   ├── categories.json
│   └── products.json
├── docs/                         # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── CONTRIBUTING.md
├── .env                          # Environment variables (not in git)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── setup.sh                      # Setup script
├── docker-compose.yml            # Docker configuration
├── Dockerfile                    # Docker image
├── manage.py                     # Django management
└── README.md                     # This file
```

## 🔗 Key URLs

| URL Pattern | View | Description |
|------------|------|-------------|
| `/` | home | Homepage with featured products |
| `/products/` | product_list | All products catalog |
| `/product/<slug>/` | product_detail | Individual product page |
| `/category/<slug>/` | category_detail | Products by category |
| `/cart/` | cart | Shopping cart |
| `/add-to-cart/<id>/` | add_to_cart | Add product to cart |
| `/update-cart/<id>/` | update_cart | Update cart quantity |
| `/remove-from-cart/<id>/` | remove_from_cart | Remove from cart |
| `/checkout/` | checkout | Checkout page |
| `/create-order/` | create_order | Process order (API) |
| `/order-success/<id>/` | order_success | Order confirmation |
| `/order-history/` | order_history | User's orders (login required) |
| `/order-detail/<id>/` | order_detail | Order details (login required) |
| `/initiate-mpesa-payment/` | initiate_mpesa | M-Pesa STK Push (API) |
| `/mpesa/callback/` | mpesa_callback | M-Pesa callback (API) |
| `/create-stripe-payment-intent/` | create_stripe_intent | Stripe payment (API) |
| `/admin/` | admin_site | Django admin panel |

## 📊 Performance & Scalability

### Optimization Techniques

**Database:**
- Database query optimization with `select_related()` and `prefetch_related()`
- Database indexes on frequently queried fields
- Connection pooling
- Query result caching

**Caching:**
- Redis for session storage
- Template fragment caching
- View caching for static content
- API response caching

**Static Files:**
- CDN integration (CloudFront/CloudFlare)
- Gzip compression
- Browser caching headers
- CSS/JS minification

**Application:**
- Async task processing with Celery
- Background jobs for email sending
- Pagination for large datasets
- Lazy loading of images

### Scalability Features

- Horizontal scaling support (multiple app servers)
- Load balancer compatible
- Database replication support
- Session storage in Redis
- Stateless application design
- Microservices-ready architecture

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write unit tests for new features
- Update documentation
- Add docstrings to functions
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django community for the excellent framework
- PayPal, Safaricom, and Stripe for payment APIs
- Bootstrap team for the UI framework
- All contributors and testers

## 📞 Support

For support, please:
- Open an issue on GitHub
- Email: support@malaikashop.com
- Documentation: https://docs.malaikashop.com

## 🔄 Changelog

### Version 2.0.0 (Current)
- ✅ Multi-payment gateway integration (PayPal, M-Pesa, Stripe)
- ✅ Enhanced order management system
- ✅ Transaction logging and monitoring
- ✅ Improved admin dashboard
- ✅ Security enhancements
- ✅ Performance optimizations
- ✅ Comprehensive documentation

### Version 1.0.0
- ✅ Basic e-commerce functionality
- ✅ PayPal integration
- ✅ Cart and checkout
- ✅ Order management

## 🗺️ Roadmap

### Version 2.1.0 (Planned)
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Advanced search with filters
- [ ] Product recommendations
- [ ] Coupon and discount system

### Version 3.0.0 (Future)
- [ ] Multi-vendor marketplace
- [ ] Real-time inventory sync
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] AI-powered product recommendations

---

**Made with ❤️ by the Malaika Team**

**⭐ Star us on GitHub if you find this project useful!**