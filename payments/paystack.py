from django.conf import settings
import requests

class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co/"

    def initialize_payment(self, amount, email, reference):
        path = 'transaction/initialize'
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "amount": int(amount * 100),  # Paystack expects kobo
            "email": email,
            "reference": reference
        }
        url = self.base_url + path
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def verify_payment(self, ref):
        path = f'transaction/verify/{ref}'
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('data'):
                return True, response_data['data']
            else:
                return False, response_data.get('message', 'verification failed')
        else:
            return False, response.json().get('message', 'Payment Verification Failed')