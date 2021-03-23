from django.urls import path, include
from .views import (MarketingPreferenceUpdateView, MailchimpWebhookView)

app_name = 'marketing'

urlpatterns = [
    path('email_setting/', MarketingPreferenceUpdateView.as_view(), name='update'),
    path('webhook/mailchimp/', MailchimpWebhookView.as_view(), name='webhook_mailchimp'),
]
