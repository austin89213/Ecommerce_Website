"""Ecommerce_Website URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from .views import home_page, about_page, HomePage
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView, TemplateView
from billing.views import payment_method_view
from django.conf import settings
from django.conf.urls.static import static
from contacts.views import contact_page

urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),
    path('', HomePage.as_view(), name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('accounts/', include("accounts.password.urls", )),
    path('account/', include("accounts.urls", namespace='accounts')),
    path('addresses/', include("addresses.urls", namespace='addresses')),
    path('billing/', include('billing.urls', namespace='billing')),
    path('carts/', include("carts.urls", namespace='carts')),
    path('marketing/', include('marketing.urls', namespace='marketing')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('products/', include("products.urls", namespace='products')),
    path('search/', include("search.urls", namespace='search')),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
