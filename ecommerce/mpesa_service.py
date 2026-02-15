# payments/mpesa_service.py
import requests
import base64
from datetime import datetime
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MPesaService:
    """Service class to handle M-Pesa Daraja API interactions"""
    
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.api_url = settings.MPESA_API_URL
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL
        self.access_token = None

    def get_access_token(self):
        """Get M-Pesa OAuth access token"""
        url = f"{self.api_url}/oauth/v1/generate?grant_type=client_credentials"
        
        auth = base64.b64encode(
            f"{self.consumer_key}:{self.consumer_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self.access_token = response.json()['access_token']
            return self.access_token
        except Exception as e:
            logger.error(f"Error getting M-Pesa access token: {str(e)}")
            raise

    def generate_password(self):
        """Generate password for STK push"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = f"{self.shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(data_to_encode.encode()).decode()
        return password, timestamp

    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """Initiate STK Push (Lipa Na M-Pesa Online)"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.api_url}/mpesa/stkpush/v1/processrequest"
        
        password, timestamp = self.generate_password()
        
        # Format phone number (remove + and leading 0, ensure 254 prefix)
        if phone_number.startswith('+'):
            phone_number = phone_number[1:]
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        if not phone_number.startswith('254'):
            phone_number = '254' + phone_number
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error initiating M-Pesa STK push: {str(e)}")
            raise

    def query_stk_push(self, checkout_request_id):
        """Query the status of an STK push transaction"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.api_url}/mpesa/stkpushquery/v1/query"
        
        password, timestamp = self.generate_password()
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error querying M-Pesa STK push: {str(e)}")
            raise

    def b2c_payment(self, phone_number, amount, occasion, remarks):
        """Make B2C payment (Business to Customer)"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.api_url}/mpesa/b2c/v1/paymentrequest"
        
        # Format phone number
        if phone_number.startswith('+'):
            phone_number = phone_number[1:]
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "InitiatorName": "your_initiator_name",
            "SecurityCredential": "your_security_credential",
            "CommandID": "BusinessPayment",
            "Amount": int(amount),
            "PartyA": self.shortcode,
            "PartyB": phone_number,
            "Remarks": remarks,
            "QueueTimeOutURL": f"{self.callback_url}timeout/",
            "ResultURL": f"{self.callback_url}result/",
            "Occasion": occasion
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error initiating M-Pesa B2C payment: {str(e)}")
            raise