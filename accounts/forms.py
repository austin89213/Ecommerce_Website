from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import EmailActivation,GuestEmail
from django.contrib import messages
from django.utils.safestring import mark_safe
User = get_user_model()


class ReactivateEmailForm(forms.Form):
    email           = forms.EmailField()
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if not qs.exists():
            signup_link = reverse("accounts:register")
            msg = """Not a registered account, please try another or <a href="{link}">sign up</a>
            """.format(link=signup_link)
            raise forms.ValidationError(mark_safe(msg))
        return email

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(label='Name', required=False)

    class Meta:
        model = User
        fields = ['full_name']

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','full_name', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Fullname'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Content'}))

    # def clean(self):
    #     all_cleaned_data = super().clean()
    #     email = all_cleaned_data['email']
    #     if 'gmail.com' not in email:
    #         raise forms.ValidationError("Email has to be gamil")
    #     return email
    #   above works as well
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gamil")
        return email

class GuestForm(forms.ModelForm):
    #email    = forms.EmailField()
    class Meta:
        model = GuestEmail
        fields = [
            'email'
        ]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GuestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # Save the provided password in hashed format
        obj = super(GuestForm, self).save(commit=False)
        if commit:
            obj.save()
            request = self.request
            request.session['guest_email_id'] = obj.id
        return obj

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False # send confirmation email to active via singals

        if commit:
            user.save()
        return user



# class RegisterForm(forms.Form):
#     username = forms.CharField()
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         qs = User.objects.filter(username=username)
#         if qs.exists():
#             raise forms.ValidationError("Username exists")
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("Email exists")
#         return email
#
#     def clean(self):
#         data =self.cleaned_data
#         password = data.get('password')
#         password2 = data.get('password2')
#         if password != password2:
#             raise forms.ValidationError("Password must match")
#         return data
