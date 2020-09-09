from django.urls import path, include
from .views import (
         ProductList,
        ProductDetail,
        ProductFeaturedList, ProductFeaturedDetail,UserProductHistoryView,UserProductHistoryPurchase,LibraryView
        )

app_name = 'products'

urlpatterns = [
    path('',ProductList.as_view(), name='list'),
    path('<slug>/',ProductDetail.as_view(),name='detail'),
    path('account/history/viewd/',UserProductHistoryView.as_view(),name='user_product_history_viewd'),
    path('account/history/purchased/',UserProductHistoryPurchase.as_view(),name='user_product_history_purchased'),
    path('account/library/',LibraryView.as_view(),name='library')
]
