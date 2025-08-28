from django.urls import path
from . import views

urlpatterns = [
    path("initiate/", views.InitiatePaymentView.as_view()),
    path("verify/", views.VerifyPaymentView.as_view()),
]