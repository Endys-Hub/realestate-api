from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('listings/', include('listings.urls')),
    path('payments/', include('payments.urls')),
    path('token-auth/', obtain_auth_token),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
