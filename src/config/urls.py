"""car_dealer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView

from apps.newsletters.views import NewsLetterView
from apps.photos.views import UpdateImageView
from common.views import logout_view, LoginAPIView, \
    RegistrationAPIView, LoginViewSimple, verify

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout_view),
    path('success/', TemplateView.as_view(template_name='success_url.html'), name='success'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('cars/', include('apps.cars.urls', namespace='cars')),
    path('login1/', LoginViewSimple.as_view(), name='login1'),
    # path('login_cust/', CustomAuthToken.as_view(), name='login_custom_token'),
    path('create/', RegistrationAPIView.as_view(), name='create'),
    path('upload-image/', login_required(UpdateImageView.as_view()), name='image-update'),
    url(r'^verify/(?P<uuid>[a-z0-9\-]+)/', verify, name='verify'),
    path('newsletter/', NewsLetterView.as_view(), name='newsletter'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
