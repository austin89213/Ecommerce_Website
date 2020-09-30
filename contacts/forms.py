from django import forms
from django.urls import reverse
from .models import Contact
class ContactForm(forms.ModelForm):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Fullname'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Content'}))
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gamil")
        return email
        
    class Meta():
        model = Contact
        fields = ('fullname','email','content')
