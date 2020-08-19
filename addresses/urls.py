from django.urls import path, include
from .views import (
        checkout_address_create_view,
        checkout_address_reuse_view
        )

app_name = 'addresses'

urlpatterns = [
    path('create/',checkout_address_create_view, name='create'),
    path('reuse', checkout_address_reuse_view,name='reuse')
]
