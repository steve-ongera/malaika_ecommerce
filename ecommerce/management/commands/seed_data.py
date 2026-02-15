"""
Django management command to seed the database with sample data.
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.core.files import File
from ecommerce.models import Category, Product
from django.contrib.auth.models import User
import random
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Seeds the database with sample categories and products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )
        parser.add_argument(
            '--images-path',
            type=str,
            default=r'C:\Users\gadaf\OneDrive\Pictures',
            help='Path to images folder (default: C:\\Users\\gadaf\\OneDrive\\Pictures)',
        )

    def handle(self, *args, **options):
        # Clear existing data if requested
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared!'))

        # Get images path
        images_path = Path(options['images_path'])
        
        # Get list of image files if path exists
        image_files = []
        if images_path.exists() and images_path.is_dir():
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            image_files = [
                f for f in images_path.iterdir() 
                if f.is_file() and f.suffix.lower() in image_extensions
            ]
            self.stdout.write(f'Found {len(image_files)} images in {images_path}')
        else:
            self.stdout.write(self.style.WARNING(
                f'Images path not found: {images_path}\n'
                f'Products will be created without images.'
            ))

        # Sample data
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest gadgets and electronic devices'
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel for everyone'
            },
            {
                'name': 'Books',
                'description': 'Books for all interests and ages'
            },
            {
                'name': 'Home & Kitchen',
                'description': 'Everything you need for your home'
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Gear for your active lifestyle'
            },
            {
                'name': 'Beauty & Personal Care',
                'description': 'Beauty products and personal care items'
            },
            {
                'name': 'Toys & Games',
                'description': 'Fun for kids and adults'
            },
            {
                'name': 'Automotive',
                'description': 'Parts and accessories for your vehicle'
            },
        ]

        products_data = {
            'Electronics': [
                {'name': 'Wireless Bluetooth Headphones', 'description': 'Premium sound quality with active noise cancellation. 30-hour battery life and comfortable fit.', 'price': 89.99, 'stock': 50},
                {'name': 'Smart Watch Fitness Tracker', 'description': 'Track your health and fitness goals. Heart rate monitor, sleep tracking, and waterproof design.', 'price': 199.99, 'stock': 30},
                {'name': 'Portable Power Bank 20000mAh', 'description': 'Fast charging power bank with dual USB ports. Perfect for travel and emergencies.', 'price': 39.99, 'stock': 100},
                {'name': 'USB-C Hub Adapter', 'description': 'Multi-port USB-C hub with HDMI, USB 3.0, and SD card reader. Compatible with laptops and tablets.', 'price': 45.99, 'stock': 75},
                {'name': 'Wireless Gaming Mouse', 'description': 'High-precision optical sensor, customizable RGB lighting, and ergonomic design for extended gaming.', 'price': 59.99, 'stock': 40},
            ],
            'Clothing': [
                {'name': 'Classic Cotton T-Shirt', 'description': 'Comfortable 100% cotton t-shirt. Available in multiple colors. Perfect for everyday wear.', 'price': 19.99, 'stock': 200},
                {'name': 'Denim Blue Jeans', 'description': 'Classic fit denim jeans with stretch comfort. Durable and stylish for any occasion.', 'price': 49.99, 'stock': 150},
                {'name': 'Lightweight Windbreaker Jacket', 'description': 'Water-resistant windbreaker with hood. Perfect for outdoor activities and light rain.', 'price': 79.99, 'stock': 60},
                {'name': 'Athletic Running Shorts', 'description': 'Breathable mesh fabric with moisture-wicking technology. Built-in liner and pockets.', 'price': 29.99, 'stock': 120},
                {'name': 'Cozy Knit Sweater', 'description': 'Soft wool blend sweater with ribbed cuffs. Warm and comfortable for cold weather.', 'price': 64.99, 'stock': 80},
            ],
            'Books': [
                {'name': 'The Art of Programming', 'description': 'Comprehensive guide to modern programming practices. From basics to advanced concepts.', 'price': 34.99, 'stock': 45},
                {'name': 'Mystery at Midnight Manor', 'description': 'Thrilling mystery novel that will keep you guessing until the last page. Perfect for mystery lovers.', 'price': 14.99, 'stock': 70},
                {'name': 'Healthy Cooking for Beginners', 'description': 'Easy and delicious recipes for a healthier lifestyle. Step-by-step instructions with photos.', 'price': 24.99, 'stock': 55},
                {'name': 'World History Encyclopedia', 'description': 'Comprehensive guide to world history from ancient times to modern day. Richly illustrated.', 'price': 49.99, 'stock': 30},
                {'name': 'Mindfulness and Meditation', 'description': 'Practical guide to mindfulness and meditation techniques. Reduce stress and improve focus.', 'price': 18.99, 'stock': 90},
            ],
            'Home & Kitchen': [
                {'name': 'Stainless Steel Knife Set', 'description': '15-piece professional knife set with wooden block. Sharp, durable, and dishwasher safe.', 'price': 89.99, 'stock': 35},
                {'name': 'Non-Stick Cookware Set', 'description': '10-piece non-stick cookware with glass lids. PFOA-free coating and oven safe up to 400°F.', 'price': 129.99, 'stock': 25},
                {'name': 'Electric Coffee Maker', 'description': 'Programmable 12-cup coffee maker with auto-shutoff. Brew your perfect cup every morning.', 'price': 59.99, 'stock': 50},
                {'name': 'Memory Foam Pillow Set', 'description': 'Set of 2 memory foam pillows with bamboo covers. Hypoallergenic and machine washable.', 'price': 44.99, 'stock': 80},
                {'name': 'LED Desk Lamp', 'description': 'Adjustable LED lamp with touch control and USB charging port. Eye-caring technology.', 'price': 32.99, 'stock': 100},
            ],
            'Sports & Outdoors': [
                {'name': 'Yoga Mat with Carrying Strap', 'description': 'Extra thick 6mm yoga mat with non-slip surface. Eco-friendly and easy to clean.', 'price': 29.99, 'stock': 70},
                {'name': 'Resistance Bands Set', 'description': 'Set of 5 resistance bands with handles and ankle straps. Perfect for home workouts.', 'price': 24.99, 'stock': 90},
                {'name': 'Camping Tent 4-Person', 'description': 'Easy setup dome tent with rainfly. Spacious interior with storage pockets and ventilation.', 'price': 149.99, 'stock': 20},
                {'name': 'Adjustable Dumbbells Pair', 'description': 'Space-saving adjustable dumbbells from 5 to 52.5 lbs. Quick-change weight selection.', 'price': 299.99, 'stock': 15},
                {'name': 'Hydration Water Bottle', 'description': 'Insulated stainless steel bottle keeps drinks cold for 24 hours. Leak-proof lid with straw.', 'price': 27.99, 'stock': 110},
            ],
            'Beauty & Personal Care': [
                {'name': 'Facial Cleansing Brush', 'description': 'Sonic facial cleansing brush with 3 speeds. Waterproof and gentle on all skin types.', 'price': 39.99, 'stock': 60},
                {'name': 'Hair Dryer Ionic Technology', 'description': 'Professional hair dryer with ionic technology for faster drying. Multiple heat and speed settings.', 'price': 54.99, 'stock': 45},
                {'name': 'Makeup Brush Set', 'description': '12-piece professional makeup brush set with case. Soft synthetic bristles for flawless application.', 'price': 29.99, 'stock': 75},
                {'name': 'Electric Toothbrush', 'description': 'Rechargeable electric toothbrush with 5 brushing modes. Smart timer and pressure sensor.', 'price': 79.99, 'stock': 50},
                {'name': 'Aromatherapy Diffuser', 'description': 'Ultrasonic essential oil diffuser with LED lights. Whisper-quiet operation and auto shut-off.', 'price': 34.99, 'stock': 85},
            ],
            'Toys & Games': [
                {'name': 'Building Blocks Set 1000 Pieces', 'description': 'Classic building blocks in assorted colors. Compatible with major brands. Ages 4+.', 'price': 39.99, 'stock': 55},
                {'name': 'Board Game Strategy Edition', 'description': 'Family-friendly strategy board game for 2-6 players. Average playtime 60 minutes.', 'price': 44.99, 'stock': 40},
                {'name': 'Remote Control Car', 'description': 'Fast RC car with 2.4GHz remote control. Rechargeable battery included. For ages 8+.', 'price': 49.99, 'stock': 35},
                {'name': 'Art & Craft Supplies Kit', 'description': 'Complete art kit with paints, brushes, markers, and paper. Perfect for young artists.', 'price': 34.99, 'stock': 65},
                {'name': 'Puzzle 1000 Pieces', 'description': 'Challenging jigsaw puzzle with beautiful artwork. Finished size 27" x 19". Ages 12+.', 'price': 19.99, 'stock': 90},
            ],
            'Automotive': [
                {'name': 'Car Phone Holder Mount', 'description': 'Universal dashboard and windshield phone mount. 360-degree rotation and one-hand operation.', 'price': 19.99, 'stock': 150},
                {'name': 'Emergency Car Kit', 'description': 'Complete roadside emergency kit with jumper cables, flashlight, and first aid supplies.', 'price': 54.99, 'stock': 40},
                {'name': 'Car Vacuum Cleaner', 'description': 'Powerful handheld car vacuum with HEPA filter. Includes multiple attachments and 16ft cord.', 'price': 44.99, 'stock': 60},
                {'name': 'Dash Camera 1080p', 'description': 'Full HD dash cam with night vision and G-sensor. Loop recording and 170-degree wide angle.', 'price': 89.99, 'stock': 35},
                {'name': 'Car Seat Organizer', 'description': 'Backseat organizer with multiple pockets and tablet holder. Kick mat protection included.', 'price': 24.99, 'stock': 80},
            ],
        }

        # Create categories
        self.stdout.write('Creating categories...')
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created category: {category.name}'))
            else:
                self.stdout.write(f'  - Category already exists: {category.name}')

        # Create products
        self.stdout.write('\nCreating products...')
        products_created = 0
        for category_name, products in products_data.items():
            category = categories[category_name]
            
            for product_data in products:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'category': category,
                        'description': product_data['description'],
                        'price': product_data['price'],
                        'stock': product_data['stock'],
                        'available': True
                    }
                )
                
                # Attach random image if available and product was just created
                if created and image_files:
                    try:
                        random_image = random.choice(image_files)
                        with open(random_image, 'rb') as img_file:
                            product.image.save(
                                random_image.name,
                                File(img_file),
                                save=True
                            )
                        self.stdout.write(self.style.SUCCESS(
                            f'  ✓ Created product: {product.name} (with image: {random_image.name})'
                        ))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            f'  ✓ Created product: {product.name} (no image - error: {str(e)})'
                        ))
                elif created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created product: {product.name}'))
                else:
                    self.stdout.write(f'  - Product already exists: {product.name}')
                
                if created:
                    products_created += 1

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('DATABASE SEEDING COMPLETED!'))
        self.stdout.write('='*60)
        self.stdout.write(f'Categories created: {len(categories)}')
        self.stdout.write(f'Products created: {products_created}')
        self.stdout.write(f'Total products in database: {Product.objects.count()}')
        self.stdout.write('\n' + self.style.SUCCESS('✓ Your e-commerce store is ready to use!'))
        self.stdout.write('  Visit http://localhost:8000/ to see your products\n')