from django.http import  HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from . forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model
from products.models import Product
from django.views.generic import ListView

class  HomePage(ListView):
    template_name ='home_page.html'

    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.all().featured()

def home_page(request):
    # print(request.session.get('user','unknown')) #seesion getter
    context = {
        'title':'Hello World',
        'content':'Welcome to the home page',
            }
    return render(request,'home_page.html',context)

def about_page(request):
    context = {
        'title':'About Page',
        'content':'Welcome to the about page'
    }
    return render(request,'home_page.html',context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title':'Contact',
        'content':'Welcome to the contact page',
        'form':contact_form,
    }
    if contact_form.is_valid():
        form_data =contact_form.cleaned_data
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message":"Thank you for submitting!"})
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
            #another way to use json
    # if request.method == 'POST':
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request,'contact/contact.html',context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    print("User logged in:")
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(request.user.is_authenticated)
        if user is not None:
            login(request, user)
            return redirect("login")
            print(request.user.is_authenticated)
        else:
            print('Invalid Login')
    return render(request,'auth/login.html',context)

User=get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username,email,password)
        print(new_user)
    return render(request,'auth/register.html',context)
