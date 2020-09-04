from django.http import  HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, FormView, DetailView,View
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from Ecommerce_Website.mixins import RequestFormAttachMixin,NextUrlMixin
from . forms import ContactForm, LoginForm, RegisterForm, GuestForm, ReactivateEmailForm
from . models import  GuestEmail, EmailActivation, User
from . signals import  user_logged_in

class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user

class AccountEmailActivateView(FormMixin,View):
    success_url = '/account/login/'
    form_class = ReactivateEmailForm
    def get(self,request,key=None,*args,**kwargs):
        qs = EmailActivation.objects.filter(key__iexact=key)
        confirm_qs = qs.confirmable()
        if confirm_qs.count() == 1:
            obj = confirm_qs.first()
            obj.activate()
            messages.success(request,"Your email has been confirmed. Please login.")
            return redirect("accounts:login")
        else:
            activated_qs = qs.filter(activated=True)
            if activated_qs.exists():
                reset_link = reverse("password_reset")
                msg = """Your email has already been confirmed
                Do you need to <a href="{link}">reset your password</a>?
                """.format(link=reset_link)
                messages.success(request, mark_safe(msg))
                return redirect("accounts:login")
        context = {'form':self.get_form()}
        return render(request,'registration/activation-error.html',context)

    def post(self,request,*args,**kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email to activate it before logging in."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user,email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView,self).form_valid(form)


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        'form': form
    }
    print("User logged in:")
    print(request.user.is_authenticated)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirct_path = next_ or next_post or None
    print(redirct_path)
    if form.is_valid():
        print(form.cleaned_data)
        email = form.cleaned_data.get('email')
        new_geust_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_geust_email.id
        if is_safe_url(redirct_path, request.get_host()):
            return redirect(redirct_path)
        else:
            return redirect('/register/')
    return redirect('/register/')

class GuestRegisterView(NextUrlMixin,  RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirct_path = next_ or next_post or None
        print(form.cleaned_data)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        user_qs = User.objects.filter(email__iexact=email)
        user_obj = user_qs.first()
        confirm_email_qs = EmailActivation.objects.filter(email=email)
        confirm_email_obj = confirm_email_qs.first()
        if not user_obj:
            signup_link = reverse("accounts:register")
            msg = """Not a registered account, please try another or <a href="{link}">sign up</a>
            """.format(link=signup_link)
            messages.success(request,mark_safe(msg))
            return super(LoginView,self).form_invalid(form)

        else:
            if not user_obj.is_active:
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                reconfirm_link = reverse("accounts:resend-activation")

                if is_confirmable:
                    msg1 = f''' This account is not activated yet!
                    Please check your email box or get another confirmration email
                    <a href="{reconfirm_link}">here</a>  '''
                    messages.success(request,mark_safe(msg1))
                    return super(LoginView,self).form_invalid(form)

                if not is_confirmable:
                    reconfirm_msg = f"""Your previous confirmration email expired. Go  <a href='{reconfirm_link}'>
                    here</a> to have another one.
                    """
                    messages.success(request,mark_safe(reconfirm_msg))
                    return super(LoginView,self).form_invalid(form)


            login(request, user)
            user_logged_in.send(user.__class__, instance=user,request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirct_path, request.get_host()):
                return redirect(redirct_path)
            else:
                return redirect('/')
        return super(LoginView,self).form_invalid(form)



class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = '/account/login/'
    success_message = """Activation link sent. Please check your email and confirm your account before logging in."""
#
# User=get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         'form': form
#     }
#     if form.is_valid():
#         form.save()
#     return render(request,'auth/register.html',context)
