"""WCF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.views.generic import RedirectView

from WCF import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/assets/img/favicon.ico', permanent=True)),
    path('', include('items.urls')),
    path('', include('account.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/dashboard', permanent=True)),
    path('purchase', include('purchase.urls')),
]

handler404 = 'helpers.views.error_404'
handler403 = 'helpers.views.error_403'
handler500 = 'helpers.views.error_500'
handler503 = 'helpers.views.error_503'

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
