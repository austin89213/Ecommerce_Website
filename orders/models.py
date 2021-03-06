from django.db import models
from django.db.models.signals import pre_save, post_save
from Ecommerce_Website.utils import unique_ordr_id_generator
from carts.models import Cart
from billing.models import BillingProfile
from products.models import Product
from addresses.models import Address
from django.urls import reverse
from Ecommerce_Website import settings
import math

User = settings.AUTH_USER_MODEL

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipeed', 'Shipped'),
    ('refunded', 'Refunded'),
)


class OrderManagerQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        order_qs = self.get_queryset().filter(
            billing_profile=billing_profile, cart=cart_obj, active=True, status='created'
        )

        if order_qs.count() == 1:
            order_obj = order_qs.first()
            created = False
        else:
            order_obj, created = self.model.objects.get_or_create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return order_obj, created


#order id should be random, unique
class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, blank=True)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', null=True, blank=True, on_delete=models.CASCADE
    )
    billing_address = models.ForeignKey(
        Address, related_name='billing_address', null=True, blank=True, on_delete=models.CASCADE
    )
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=60, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp', '-updated']

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'order_id': self.order_id})

    def get_status(self):
        if self.status == 'created':
            return "Not paid yet"
        if self.status == 'paid':
            return "Paid and will be shipping soon"
        if self.status == 'shipeed':
            return 'shipped'
        if self.status == 'refunded':
            return 'refunded'

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_new_total = format(new_total, '.2f')
        self.total = new_total
        self.save()
        return new_total

    def check_done(self):
        shipping_address_required = not self.cart.is_digital
        shipping_done = False
        if shipping_address_required and self.shipping_address:
            shipping_done = True
        elif shipping_address_required and not self.shipping_address:
            shipping_done = False
        else:
            shipping_done = True
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        shipping_address = self.shipping_address
        total = self.total
        if billing_profile and billing_address and shipping_done and total > 0:
            return True
        return False

    def update_purchases(self):
        for p in self.cart.products.all():
            obj, created = ProductPurchase.objects.get_or_create(
                order_id=self.order_id, product=p, billing_profile=self.billing_profile
            )
        return ProductPurchase.objects.filter(order_id=self.order_id).count()

    def mark_paid(self):
        if self.status != 'paid':
            if self.check_done():
                self.status = 'paid'
                self.save()
                self.update_purchases()
        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_ordr_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


# Generate the order id
# Generate the order total
def post_save_order(sender, instance, created, *args, **kwargs):
    print('running')
    if created:
        print('updating')
        instance.update_total()


post_save.connect(post_save_order, sender=Order)


class ProductPurchaseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)

    def refunded(self):
        return self.filter(refunded=True)

    def digital(self):
        return self.filter(product__is_digital=True)

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def products_by_request(self, request):
        qs = self.by_request(request)
        prodcuts_purchased_ids = [x.product.id for x in qs]
        prodcuts_qs = Product.objects.filter(id__in=prodcuts_purchased_ids).distinct()
        return prodcuts_qs


class ProductPurchaseManager(models.Manager):
    def get_queryset(self):
        return ProductPurchaseQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def refunded(self):
        return self.get_queryset().refunded()

    def digital(self):
        return self.get_queryset().active().digital()

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def products_by_request(self, request):
        qs = self.by_request(request)
        prodcuts_purchased_ids = [x.product.id for x in qs]
        prodcuts_qs = Product.objects.filter(id__in=prodcuts_purchased_ids).distinct()
        return prodcuts_qs


class ProductPurchase(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchased')
    refunded = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProductPurchaseManager()

    def __str__(self):
        return self.product.title
