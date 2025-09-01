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
