"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("users.urls"), name="users"),
    path('contactmessage/', include("contactmessages.urls"), name="contactmessages"),
    path('files/', include('car_images.urls'), name='car_images'),  # dökümantasyon'da image'lerin url'si icin files/ kullanmamizi istiyor...
    path('car/', include('cars.urls'), name='cars'),
]

if settings.DEBUG:    # static'i ve settings'i yukarida import ettik.
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
