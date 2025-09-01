from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Listing, Enquiry
from .serializers import ListingSerializer, EnquirySerializer

class ListingListView(APIView):
    """
    GET:
        - Users see only published & available listings
        - Admin/staff see all listings
    POST:
        - Only staff can create a new listing
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return []  # Anyone can view
        return [IsAuthenticated()]  # Require auth for POST

    def get(self, request):
        try:
            if request.user.is_staff:
                listings = Listing.objects.all()
            else:
                listings = Listing.objects.filter(is_published=True, is_available=True)
            
            # Search functionality
            search_query = request.query_params.get('search', None)
            if search_query:
                listings = listings.filter(title__icontains=search_query) | listings.filter(description__icontains=search_query)    

            serializer = ListingSerializer(listings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            # enforce staff-only
            if not request.user.is_staff:
                return Response(
                    {"detail": "Only staff users can create listings."},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = ListingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListingDetailView(APIView):
    
    def get(self, request, pk):
        try:
            listing = get_object_or_404(Listing, pk=pk)
            serializer = ListingSerializer(listing)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff can update listings."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            listing = get_object_or_404(Listing, pk=pk)
            serializer = ListingSerializer(listing, data=request.data, partial=True)  # partial=True lets you update only provided fields
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            if not request.user.is_staff:
                return Response(
                    {"error": "Only staff can delete listings."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            listing = get_object_or_404(Listing, pk=pk)
            listing.delete()
            return Response(
                {"message": "Listing deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class ListingPaymentView(APIView):
    """
    POST payment for a listing
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            listing = get_object_or_404(Listing, pk=pk)

            if not listing.is_available:
                return Response({"detail": "Listing not available."}, status=status.HTTP_400_BAD_REQUEST)

            # Mock payment success (integration with Paystack/Stripe can go here)
            listing.is_available = False
            listing.save()

            return Response({"detail": "Payment successful. Listing marked as unavailable."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EnquiryView(APIView):
    """
    POST create enquiry
    GET all enquiries for admin
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if not request.user.is_staff:
                return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

            enquiries = Enquiry.objects.all()
            serializer = EnquirySerializer(enquiries, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = EnquirySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
