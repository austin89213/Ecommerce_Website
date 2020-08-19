from django.http import  HttpResponse
from django.shortcuts import render,redirect
from . forms import ContactForm, LoginForm, RegisterForm, GuestForm
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url
from .models import  GuestEmail
from django.views.generic import CreateView, FormView
from . signals import  user_logged_in
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
    return redirect('/registe/')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirct_path = next_ or next_post or None
        print(form.cleaned_data)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
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

# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         'form': form
#     }
#     print("User logged in:")
#     print(request.user.is_authenticated)
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirct_path = next_ or next_post or None
#     print(redirct_path)
#     if form.is_valid():
#         print(form.cleaned_data)
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirct_path, request.get_host()):
#                 return redirect(redirct_path)
#             else:
#                 return redirect('/')
#         else:
#             print('Invalid Login')
#     return render(request,'accounts/login.html',context)



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/login/'
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
