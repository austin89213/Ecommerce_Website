from django.urls import include, path
from django.conf.urls import url
from .views import (LoginView, RegisterView, guest_register_view,GuestRegisterView,
                    AccountHomeView, AccountEmailActivateView, UserDetailChangeView)
from django.contrib.auth.views import LogoutView, LoginView as builtinLoginView
from products.views import UserProductHistoryView
app_name = 'accounts'
urlpatterns=[
    path('login/',LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/guest/',GuestRegisterView.as_view(), name='guest_register'),
    path('home/',AccountHomeView.as_view(),name='home'),
    path('details/update/',UserDetailChangeView.as_view(),name='user_update'),
    path('email/resend-activation/',AccountEmailActivateView.as_view(),
                                                name='resend-activation'),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$',AccountEmailActivateView.as_view(),
                                                name='email-activate'),

]
