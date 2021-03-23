from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class WelcomePage(TemplateView):
    template_name = 'welcome.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("thanks"))
        return super().get(request, *args, **kwargs)
