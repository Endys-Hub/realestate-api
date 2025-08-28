from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
from django.conf import settings
from .models import Listing, Payment

from django.shortcuts import get_object_or_404
from .serializers import PaymentSerializer

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY

class InitiatePaymentView(APIView):
    def post(self, request):
        try:
            listing_id = request.data.get("listing_id")
            listing = Listing.objects.get(id=listing_id, is_available=True)

            # generate payment reference
            import uuid
            reference = str(uuid.uuid4())

            # create payment object
            payment = Payment.objects.create(
                user=request.user,
                listing=listing,
                amount=listing.price,  # assuming Listing has price field
                reference=reference,
            )

            # call Paystack initialize endpoint
            headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
            data = {
                "email": request.user.email,
                "amount": int(listing.price * 100),  # Paystack expects kobo
                "reference": reference,
                "callback_url": "http://localhost:8000/payments/verify/",
            }
            response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)
            res_data = response.json()

            if res_data.get("status"):
                return Response(res_data["data"], status=status.HTTP_200_OK)
            return Response(res_data, status=status.HTTP_400_BAD_REQUEST)

        except Listing.DoesNotExist:
            return Response({"error": "Listing not available"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    def get(self, request):
        reference = request.query_params.get("reference")
        headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
        url = f"https://api.paystack.co/transaction/verify/{reference}"

        response = requests.get(url, headers=headers)
        res_data = response.json()

        if res_data.get("status") and res_data["data"]["status"] == "success":
            try:
                payment = Payment.objects.get(reference=reference)
                payment.status = "success"
                payment.save()

                # mark listing as unavailable
                payment.listing.is_available = False
                payment.listing.save()

                return Response({"message": "Payment verified successfully"}, status=status.HTTP_200_OK)
            except Payment.DoesNotExist:
                return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(res_data, status=status.HTTP_400_BAD_REQUEST)

