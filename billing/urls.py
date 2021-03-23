from django.urls import path, include
from .views import payment_method_create_view, payment_method_view

app_name = 'billing'

urlpatterns = [
    path('payment-method/', payment_method_view, name='payment_method'),
    path('payment-method/create/', payment_method_create_view, name='payment_method_create'),
]
