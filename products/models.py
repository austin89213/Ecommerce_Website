from django.db import models
import os
import random
from Ecommerce_Website.utils import random_string_generator,unique_slug_generator
from django.db.models.signals import pre_save,post_save,m2m_changed
from django.urls import reverse
from django.db.models import Q
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance,filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1,9999999)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"products/{instance.title}/{final_filename}"

# Create your models here.

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self): #Product.objects.all.featured()
        return self.filter(featured=True, active=True)

    def search(self,query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(price__icontains=query)|
                   Q(tag__title__icontains=query)
                   )
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Product.objects.featured()
        return self.get_queryset().filter(featured=True)

    def get_by_pk(self,pk): #Prodcut.objects == self.get_queryset()
        qs = self.get_queryset().filter(pk=pk)
        if qs.count() == 1:
            return qs

    def search(self,query):
        return self.get_queryset().search(query)

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=20)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    # def get_absolute_url(self):
    #     return "/products/{slug}".format(slug=self.slug)
    def get_absolute_url(self):
        return reverse('products:detail',kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title

def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)
# pre_save means the method is going to run before the data of models saved
