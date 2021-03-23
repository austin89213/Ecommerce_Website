from django.shortcuts import render, redirect, reverse
from .utils import Mailchimp
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from django.views import generic
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from .mixins import CsrfExemptMixin

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, generic.UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_message = "Your email preference has been updated. Thank you!"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/accounts/login/?next=/marketing/email_setting/")
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preference'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj

    def get_success_url(self):
        return self.request.path


"""
POST METHOD
"root":
"type": "unsubscribe"
"fired_at": "2020-08-17 03:41:28"
"data":
"reason": "manual"
"id": "cc32375305"
"email": "augustinecoding@gmail.com"
"email_type": "html"
"ip_opt": "1.165.108.159"
"web_id": "165483050"
"merges":
"EMAIL": "augustinecoding@gmail.com"
"FNAME": "Augustine"
"LNAME": "Lin"
"ADDRESS": ""
"PHONE": ""
"BIRTHDAY": ""
"list_id": "703f52d0ce"
"""


class MailchimpWebhookView(CsrfExemptMixin, generic.View):  #HTTP GET -- def get()
    def get(self, request, *args, **kwargs):
        return HttpResponse("Thank you", status=200)

    def post(self, request, *args, **kwargs):
        data = request.POST  #usually a dictionary
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get('data[email]')
            response_status, response = Mailchimp.change_subscription_status(email)
            sub_status = response['status']
            is_subscribed = None
            mailchimp_subscribed = None
            if sub_status == 'subscribed':
                is_subscribed, mailchimp_subscribed = (True, True)
            elif sub_status == 'ubsubscribed':
                is_subscribed, mailchimp_subscribed = (False, False)
            if is_subscribed is not None and mailchimp_subscribed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                        subscribed=is_subscribed, mailchimp_subscribed=mailchimp_subscribed, mailchimp_msg=str(data)
                    )
        return HttpResponse("Thank you", status=200)
