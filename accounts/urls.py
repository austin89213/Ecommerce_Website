from django.urls import include, path
from .views import LoginView,RegisterView,guest_register_view
from django.contrib.auth.views import LogoutView
app_name = 'accounts'
urlpatterns=[
    path('login/',LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/guest',guest_register_view, name='guest_register'),

]
