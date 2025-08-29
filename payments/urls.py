from django.urls import path
from . import views

urlpatterns = [
    path("initiate/<int:listing_id>/", views.InitiatePaymentView.as_view()),
    path("verify/<str:reference>/", views.VerifyPaymentView.as_view()),
]