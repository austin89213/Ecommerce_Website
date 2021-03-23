from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.db.models import Q
from Ecommerce_Website.utils import random_string_generator, unique_key_generator
# Create your models here.
# send_mail(subject,message,from_email,recipient_list,html_message)
DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a passowrd")
        if not full_name:
            raise ValueError("Users must have a fullname")
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user_obj.set_password(password)  #change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name=None, password=None):
        staff_user = self.create_user(
            email=email,
            full_name=full_name,
            password=password,
            is_staff=True,
        )
        return staff_user

    def create_superuser(self, email, full_name=None, password=None):
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
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    staff = models.BooleanField(default=False)  # staff
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Join Time')
    is_active = models.BooleanField(default=True)
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

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class EmailActivationQuerySet(models.query.QuerySet):  #EmailActivation.objects.all().confirmable()
    def confirmable(self):
        DEFAULT_ACTIVATION_DAYS
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        #dose my object have a timestamp in this range
        end_range = now
        return self.filter(activated=False,
                           forced_expired=False).filter(timestamp__gt=start_range, timestamp__lte=end_range)


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(Q(email=email) | Q(user__email=email)).filter(activated=False)


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)  #7days
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, "BASE_URL", 'https://austin-ecommerce.herokuapp.com/')
                key_path = reverse("accounts:email-activate", kwargs={'key': self.key})
                path = f"{base_url}{key_path}"
                context = {
                    'path': path,
                    'email': self.email,
                }

                txt_ = get_template("accounts/emails/verify.txt").render(context)
                html_ = get_template("accounts/emails/verify.html").render(context)
                subject = '1-click Email Verification'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email, from_email]
                sent_eamil = send_mail(
                    subject=subject,
                    message=txt_,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    html_message=html_,
                    fail_silently=False,
                )
                return sent_eamil
        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()


post_save.connect(post_save_user_create_reciever, sender=User)


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=EmailActivation)
