from django.urls import path, include
from .views import (
        product_list, ProductList,
        product_detail,ProductDetail,
        ProductFeaturedList, ProductFeaturedDetail,
        )

app_name = 'products'

urlpatterns = [
    path('',ProductList.as_view(), name='list'),
    path('<slug>/',ProductDetail.as_view(),name='detail'),
]
