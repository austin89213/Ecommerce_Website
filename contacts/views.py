from django.http import  HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from . forms import ContactForm
from .models import Contact
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title':'Contact',
        'content':'Welcome to the contact page',
        'form':contact_form,
    }
    if contact_form.is_valid():
        Contact=contact_form.save()
        form_data =contact_form.cleaned_data
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message":"Thank you for submitting!"})
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request,'contacts/contact.html',context)
# def register(request):
#
#     registerd = False
#
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileInfoForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save() # save the form to database
#             user.set_password(user.password) #hashing the password
#             user.save() #resave the password
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'profile_pic' in request.FILES:
#                 profile.profile_pic = request.FILES['profile_pic']
#
#             profile.save()
#
#             registerd = True
#
#         else: #either user_form or profile_form is not valid
#             print(user_form.errors,profile_form.errors)
#     else: #request.method is not 'POST' or no request
#         user_form=UserForm()
#         profile_form = UserProfileInfoForm()
#
#     return render(request,'basic_app/registration.html',
#                                 {'user_form':user_form,
#                                     'profile_form':profile_form,
#                                     'registerd':registerd})
