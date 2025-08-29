from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Payment
from listings.models import Listing
from .paystack import Paystack
import uuid
from rest_framework.permissions import IsAuthenticated #

class InitiatePaymentView(APIView):

    permission_classes = [IsAuthenticated]   # Require login
    def post(self, request, listing_id):
        """Initialize Paystack payment for a listing"""
        listing = get_object_or_404(Listing, id=listing_id, is_available=True)

        # Generate unique reference
        reference = str(uuid.uuid4()).replace("-", "")[:12]

        # Create a Payment record
        payment = Payment.objects.create(
            user=request.user,
            listing=listing,
            amount=listing.price,
            reference=reference
        )

        paystack = Paystack()
        response_data = paystack.initialize_payment(
            amount=payment.amount,
            email=request.user.email,
            reference=payment.reference
        )

        if response_data.get("status"):
            return Response(
                {
                    "payment_id": payment.id,
                    "authorization_url": response_data["data"]["authorization_url"],
                    "access_code": response_data["data"]["access_code"],
                    "reference": payment.reference
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": response_data.get("message", "Payment initialization failed")},
                status=status.HTTP_400_BAD_REQUEST
            )


class VerifyPaymentView(APIView):

    permission_classes = [IsAuthenticated]   # Require login
    def get(self, request, reference):
        """Verify Paystack payment"""
        payment = get_object_or_404(Payment, reference=reference)

        paystack = Paystack()
        success, result = paystack.verify_payment(reference)

        if success and result["status"] == "success":
            payment.status = "success"
            payment.save()

            # Mark listing as unavailable
            payment.listing.is_available = False
            payment.listing.save()

            return Response(
                {"message": "Payment successful", "listing": payment.listing.id},
                status=status.HTTP_200_OK
            )
        else:
            payment.status = "failed"
            payment.save()
            return Response(
                {"error": result},
                status=status.HTTP_400_BAD_REQUEST
            )


'''
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
'''