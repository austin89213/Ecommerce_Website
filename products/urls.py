from django.urls import path, include
from .views import (
         ProductList,
        ProductDetail,
        ProductFeaturedList, ProductFeaturedDetail,UserProductHistoryView
        )

app_name = 'products'

urlpatterns = [
    path('',ProductList.as_view(), name='list'),
    path('<slug>/',ProductDetail.as_view(),name='detail'),
    path('account/history/',UserProductHistoryView.as_view(),name='user_product_history'),

]
