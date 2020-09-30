from django.urls import path, include
from .views import (
        cart_update,
        cart_home,
        checkout_home,
        checkout_done,
        cart_detail_api_view
        )

app_name = 'carts'

urlpatterns = [
    path('',cart_home, name='home'),
    path('update/',cart_update,name='update'),
    path('checkout/',checkout_home,name='checkout'),
    path('checkout/success',checkout_done,name='success'),
    path('api/carts',cart_detail_api_view,name="api_carts"),
]
