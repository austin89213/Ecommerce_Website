from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from accounts.models import GuestEmail
from django.urls import reverse
from django.conf import settings
import stripe

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_4eC39HqLyjWDarjtT1zdp7dc")
stripe.api_key = STRIPE_SECRET_KEY
User = get_user_model()
# Create your models here.


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        billing_guest_profile_created = False
        billing_profile = None
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            billing_profile, billing_profile_created = self.model.objects.get_or_create(user=user, email=user.email)

        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            billing_profile, billing_guest_profile_created = self.model.objects.get_or_create(
                email=guest_email_obj.email
            )
        else:
            pass

        return billing_profile, billing_guest_profile_created


class BillingProfile(models.Model):
    user = models.OneToOneField(
        User, unique=True, null=True, blank=True, on_delete=models.CASCADE, related_name='billing_profile'
    )
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj, card=None):
        return Charge.objects.do_charge(self, order_obj, card)

    def get_cards(self):  #Card.objects.filter(billing_profile=self,active=True)
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse('billing:payment_method')

    @property
    def has_card(self):
        card_qs = self.get_cards()
        return card_qs.exists()  #True or False

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("Sending to stripe/briantree")
        customer = stripe.Customer.create(source='tok_mastercard', email=instance.email)
        print(customer)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)


class CardManager(models.Manager):
    def all(self, *args, **kwargs):  #ModedlClass.objects.all() --> ModelClass.objects.filter(active=True)
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            stripe_card_response = customer.create_source(customer.id, source=token)
            new_card = self.model(
                billing_profile=billing_profile,
                customer_id=customer.id,
                stripe_id=stripe_card_response.id,
                brand=stripe_card_response.brand,
                country=stripe_card_response.country,
                exp_month=stripe_card_response.exp_month,
                exp_year=stripe_card_response.exp_year,
                last4=stripe_card_response.last4
            )
            new_card.save()
            return new_card
        return None


class Card(models.Model):

    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    brand = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    last4 = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CardManager()

    def __str__(self):
        return f'{self.brand}{self.last4}'


def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)


post_save.connect(new_card_post_save_receiver, sender=Card)


class ChargeManager(models.Manager):
    def do_charge(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)  # card_obj.billing_profile
            print(f'cards are: {cards}')
            if cards.exists():
                card_obj = cards.first()
                print(card_obj)
        if card_obj is None:
            return False, "No cards Available"
        c = stripe.Charge.create(
            amount=int(order_obj.total * 100),
            currency="usd",
            customer=billing_profile.customer_id,
            source=card_obj.stripe_id,
            metadata={"order_id": order_obj.order_id}
        )
        new_charge_obj = self.model(
            billing_profile=billing_profile,
            customer_id=c.customer,
            card_id=c.payment_method,
            stripe_id=c.stripe_id,
            paid=c.paid,
            refunded=c.refunded,
            outcome=c.outcome,
            outcome_type=c.outcome.get('type'),
            seller_message=c.outcome.get('seller_message'),
            risk_level=c.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    card_id = models.CharField(max_length=120, null=True, blank=True)
    stripe_id = models.CharField(max_length=120)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()
