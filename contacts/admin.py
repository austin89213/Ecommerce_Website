from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ['fullname', 'email', 'content']

    class Meta:
        model = Contact
        fields = ['fullname', 'email', 'content']


admin.site.register(Contact, ContactAdmin)
# Register your models here.
