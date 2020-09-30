from django.db import models
from django.urls import reverse
# Create your models here.
class Contact(models.Model):
    fullname = models.CharField(max_length=60)
    email = models.EmailField()
    content = models.CharField(max_length=252)

    def __str__(self):
        return f'{self.email} said: {self.content}'
