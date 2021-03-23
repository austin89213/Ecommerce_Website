from django.urls import path, include
from .views import SearchProductList

app_name = 'search'

urlpatterns = [
    path('', SearchProductList.as_view(), name='query'),
]
