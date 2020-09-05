from django.urls import include, path
from .views import OrderListView, OrderDetailView
app_name = 'orders'
urlpatterns=[
    path('list/',OrderListView.as_view(),name='list'),
    path('<order_id>/',OrderDetailView.as_view(),name='detail'),

]
