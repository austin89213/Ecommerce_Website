from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save,post_save,m2m_changed
from products.models import Product
from decimal import Decimal
# Create your models here.

User = get_user_model()

class CartManager(models.Manager):
    def new_or_get(self,request):
        print('Cart_view working')
        cart_id = request.session.get("cart_id",None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count()==1:
            new_obj = False
            cart_obj = qs.first()
            print('Cart ID exist:')
            print(request.session['cart_id'])
            if request.user.is_authenticated and cart_obj.user == None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = self.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
            print('New Cart ID created:')
            print(request.session['cart_id'])

        return cart_obj, new_obj

    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        print(f'user_obj {user_obj}')
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user      = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    products  = models.ManyToManyField(Product,blank=True)
    subtotal  = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    total     = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)
    objects = CartManager()
    def __str__(self):
        return str(self.id)
    def tax(self):
        return self.total - self.subtotal

    @property
    def is_digital(self):
        qs = self.products.all()
        new_qs = qs.filter(is_digital=False)
        if new_qs.exists():
            return False
        return True


def cart_m2m_changed_eceiver(sender,instance,action,*args,**kwargs):
    if action =='post_add' or action == 'post_remove' or action == 'post_clear':
        print(action)
        print(instance.products.all())
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        instance.subtotal = total
        instance.save()
        print(instance.total)
m2m_changed.connect(cart_m2m_changed_eceiver,sender=Cart.products.through)


def cart_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.08) #8% tax
    else:
        instance.total = 0

pre_save.connect(cart_pre_save_receiver, sender=Cart)
