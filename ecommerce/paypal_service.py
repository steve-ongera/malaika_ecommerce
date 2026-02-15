# payments/paypal_service.py
import requests
import base64
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class PayPalService:
    """Service class to handle PayPal API interactions"""
    
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.api_url = settings.PAYPAL_API_URL
        self.access_token = None

    def get_access_token(self):
        """Get PayPal OAuth access token"""
        url = f"{self.api_url}/v1/oauth2/token"
        
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            self.access_token = response.json()['access_token']
            return self.access_token
        except Exception as e:
            logger.error(f"Error getting PayPal access token: {str(e)}")
            raise

    def create_order(self, amount, currency='USD', order_id=None):
        """Create a PayPal order"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.api_url}/v2/checkout/orders"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": str(order_id) if order_id else "default",
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                }
            }],
            "application_context": {
                "brand_name": "Malaika Shop",
                "landing_page": "BILLING",
                "user_action": "PAY_NOW",
                "return_url": f"{settings.SITE_URL}/payment/paypal/success/",
                "cancel_url": f"{settings.SITE_URL}/payment/paypal/cancel/"
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating PayPal order: {str(e)}")
            raise

    def capture_order(self, paypal_order_id):
        """Capture payment for a PayPal order"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.api_url}/v2/checkout/orders/{paypal_order_id}/capture"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error capturing PayPal order: {str(e)}")
            raise

    def get_order_details(self, paypal_order_id):
        """Get details of a PayPal order"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.api_url}/v2/checkout/orders/{paypal_order_id}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting PayPal order details: {str(e)}")
            raise

    def refund_payment(self, capture_id, amount=None, currency='USD'):
        """Refund a captured payment"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.api_url}/v2/payments/captures/{capture_id}/refund"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        payload = {}
        if amount:
            payload = {
                "amount": {
                    "value": str(amount),
                    "currency_code": currency
                }
            }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error refunding PayPal payment: {str(e)}")
            raise