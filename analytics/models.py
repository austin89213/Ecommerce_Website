from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from products.models import Product
from accounts.signals import user_logged_in
from . import utils
from .signals import object_viewed_signal
from .utils import get_client_ip

User = get_user_model()

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_SESSION = getattr(settings, 'FORCE_INACTIVE_USER_SESSION', False)


class ObjectViewedQuerySet(models.query.QuerySet):
    def by_model(self, model_class, return_model_queryset=False):
        c_type = ContentType.objects.get_for_model(model_class)
        qs = self.filter(content_type=c_type)
        if return_model_queryset:
            viewd_ids = [x.object_id for x in qs]
            return model_class.objects.filter(pk__in=viewd_ids)
        return qs


class ObjectViewedManager(models.Manager):
    def get_queryset(self):
        return ObjectViewedQuerySet(self.model, using=self._db)

    def by_model(self, model_class, return_model_queryset=False):
        return self.get_queryset().by_model(model_class, return_model_queryset)


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)  # User instance
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE
    )  # trying to get User, Product,Order,Cart,Address etc...
    object_id = models.PositiveIntegerField()  # User id, Product id, Order id,
    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )  # Product instance
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ObjectViewedManager()

    def __str__(self):
        return f'{self.content_object} viewd at {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']  #most recent saved show up first
        verbose_name = 'Object viewd'
        verbose_name_plural = 'Object viewd'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)  # == instance.__class__
    user = None
    print(sender)
    print(instance)
    print(request)
    print(request.user)
    if request.user.is_authenticated:
        user = request.user
    new_view_obj = ObjectViewed.objects.create(
        user=user, ip_address=get_client_ip(request), content_type=c_type, object_id=instance.id
    )


object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)  # User instance
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.ended = True
            self.active = False
            self.save()
        except:
            pass
        return self.ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=True).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()


if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)


def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance, ended=False, active=True)
            for i in qs:
                i.end_session()


if FORCE_INACTIVE_USER_SESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    print(instance)
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(user=user, ip_address=ip_address, session_key=session_key)


user_logged_in.connect(user_logged_in_receiver)
