from django.urls import path
from . import views

urlpatterns = [
    # Listings
    path('all/', views.ListingListView.as_view()),
    path('single/<int:pk>/', views.ListingDetailView.as_view()),
    path('payments/<int:pk>/pay/', views.ListingPaymentView.as_view()),
    path('listings/', views.ListingListView.as_view()),
    path('listings/<int:pk>/', views.ListingDetailView.as_view()),
    path('listings/<int:id>/enquiries/', views.EnquiryView.as_view()),

    # Enquiries
    path('enquiries/', views.EnquiryView.as_view()),
]




