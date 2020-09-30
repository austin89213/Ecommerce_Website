from django.db import models
import os
import random
from django.conf import settings
from Ecommerce_Website.utils import random_string_generator,unique_slug_generator,get_filename
from django.db.models.signals import pre_save,post_save,m2m_changed
from django.urls import reverse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from Ecommerce_Website.aws.utils import ProtectedRootS3BotoStorage
from Ecommerce_Website.aws.download.utils import AWSDownload
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
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True, unique=True)
    description     = models.TextField(blank=True)
    price           = models.DecimalField(decimal_places=2,max_digits=20)
    image           = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured        = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    is_digital      = models.BooleanField(default=False) # User Libary

    objects = ProductManager()

    # def get_absolute_url(self):
    #     return "/products/{slug}".format(slug=self.slug)
    def get_absolute_url(self):
        return reverse('products:detail',kwargs={'slug':self.slug})

    def __str__(self):
        if self.is_digital:
            return str(f'{self.title} [Digital]')
        return self.title
    @property
    def name(self):
        return self.title

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs

def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)
# pre_save means the method is going to run before the data of models saved

def upload_product_file_location(instance, filename):
    slug = instance.product.slug
    #id_ = 0
    id_ = instance.id
    if id_ is None:
        ProductFileClass = instance.__class__
        qs = ProductFileClass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id + 1
        else:
            id_ = 0
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = "products/{slug}/{id}/".format(slug=slug, id=id_)
    return location + filename


class ProductFile(models.Model):
    product     = models.ForeignKey(Product,on_delete=models.CASCADE)
    name        = models.CharField(max_length=120,null=True, blank=True)
    file        = models.FileField(upload_to=upload_product_file_location,
                        storage=ProtectedRootS3BotoStorage(),
                        # FileSystemStorage(location=settings.PROTECTED_ROOT)
                        )
    filepath    = models.TextField
    free        = models.BooleanField(default=False)
    user_required =models.BooleanField(default=False)

    def __str__(self):
        return str(self.file.name)

    @property
    def display_name(self):
        ori_name = os.path.basename(self.file)
        if self.name:
            return self.name
        return ori_name

    def get_default_url(self):
        return self.product.get_absolute_url()

    def generate_download_url(self):
        bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
        region = getattr(settings, 'S3DIRECT_REGION')
        access_key = getattr(settings, 'AWS_ACCESS_KEY_ID')
        secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
        if not secret_key or not access_key or not bucket or not region:
            return "/product-not-found/"
        PROTECTED_DIR_NAME = getattr(settings, 'PROTECTED_DIR_NAME', 'protected')
        path = f'{PROTECTED_DIR_NAME}/{str(self.file)}'
        print(path)

        aws_dl_object =  AWSDownload(access_key, secret_key, bucket, region)
        file_url = aws_dl_object.generate_url(path)
        return file_url

    def get_download_url(self):
        return reverse("products:download",kwargs={"slug":self.product.slug,"pk":self.pk})
