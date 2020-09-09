from django.shortcuts import render,redirect
from .models import Cart
from products.models import  Product
from django.views import generic
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from billing.models import BillingProfile
from addresses.forms import AddressForm
from addresses.models import Address
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.conf import settings

# Stripe
import stripe
STRIPE_SECRET_KEY = getattr(settings,"STRIPE_SECRET_KEY", "sk_test_4eC39HqLyjWDarjtT1zdp7dc")
STRIPE_PUB_KEY = getattr(settings,"STRIPE_PUB_KEY", 'pk_test_TYooMQauvdEDq54NiTphI7jx')
stripe.api_key = STRIPE_SECRET_KEY
# Create your views here.


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
            "ud":x.id,
            "url":x.get_absolute_url(),
            "name":x.name,
            "price":x.price,
            }
    for x in cart_obj.products.all()]
    # products_list =[]
    # for x in cart_obj.products.all():
    #     products_list.append(
    #         {"name":x.name,"price":x.price}
    #     )
    cart_data ={"products":products,"subtotal":cart_obj.subtotal,"total":cart_obj.total,"tax":cart_obj.tax()}
    return JsonResponse(cart_data)

def cart_update(request):
    product_id = request.POST.get('product_id')

    if product_id:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product does not exist")
            raise("Producr does not exist")
            return redirect("carts:home")
        else:
            cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            product_added = False
        else:
            cart_obj.products.add(product_obj) # cart_obj.products.add(1)
            product_added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax(): #Asynchronous JavaScript Anx XML / JSON(JaveScrtip Object Notation)
            print("Ajax request")
            json_data = {
                "productAdded":product_added,
                "productRemoved":not product_added,
                "cartItemCount":cart_obj.products.count()
            }
            return JsonResponse(json_data, status=200)
            # return JsonResponse({"message":"Error 400"}, status_code=400) # to test the jqeury confirm

    return redirect("carts:home")

def checkout_home(request):
    cart_obj, new_cart = Cart.objects.new_or_get(request)
    order_obj = None
    print(f'cheching out: cart{cart_obj}')
    if new_cart or cart_obj.products.count()==0 :
        return redirect('carts:home')
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm(request=request)
    address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id',None)

    shipping_address_required = not cart_obj.is_digital
    shipping_address_id = request.session.get('shipping_address_id',None)

    billing_address_form = AddressForm()
    order_qs = Order.objects.filter(cart=cart_obj, active=True)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card


    if request.method == "POST":
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            if not billing_profile.user:
                billing_profile.set_cards_inactive()
            print(f"did_charge:{did_charge},{crg_msg}")
            return redirect("carts:success")
        else:
            print(crg_msg)
            return redirect("carts:checkout")

    context ={
        "object":order_obj,
        "billing_profile":billing_profile,
        "login_form":login_form,
        "guest_form":guest_form,
        "address_form":address_form,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "has_card":has_card,
        "publish_key":STRIPE_PUB_KEY,
        "shipping_address_required":shipping_address_required,
    }
    return render(request,"carts/checkout.html",context)

def checkout_done(request):
    return render(request,"carts/checkout_done.html",{})

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    print (f'Cart is digital:{cart_obj.is_digital}')
    return render(request,"carts/home.html",{"cart":cart_obj})
