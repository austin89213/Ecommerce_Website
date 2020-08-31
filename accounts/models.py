from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self,email,full_name=None,password=None,is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a passowrd")
        if not full_name:
            raise ValueError("Users must have a fullname")
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
        )
        user_obj.set_password(password) #change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email,full_name=None,password=None):
        staff_user = self.create_user(
                    email=email,
                    full_name=full_name,
                    password=password,
                    is_staff=True,
                    )
        return staff_user

    def create_superuser(self,email,full_name=None,password=None):
        super_user = self.create_user(
                    email=email,
                    full_name=full_name,
                    password=password,
                    is_staff=True,
                    is_admin=True,
                    )
        return super_user
#keep custom User as simple as possible
#It could be very messy to change it
class User(AbstractBaseUser):
    email       = models.EmailField(unique=True,max_length=255)
    full_name   = models.CharField(max_length=255, blank=True, null=True)
    staff       = models.BooleanField(default=False) # staff
    admin       = models.BooleanField(default=False) # superuser
    timestamp   = models.DateTimeField(auto_now_add=True, verbose_name='Join Time')
    is_active   = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    # email and password are required by default
    REQUIRED_FIELDS = ['full_name']
    #things from python manage.py createsuperuser will be in here
    objects = UserManager()
    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin



class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
