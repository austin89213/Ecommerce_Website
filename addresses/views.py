from django.shortcuts import render
from .forms import AddressForm
from .models import Address
from django.views import generic
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect
from billing.models import BillingProfile
from .models import Address


# Create your views here.
class AddressCreate(generic.CreateView):
    form = AddressForm()
    template_name = 'addresses/snippets/address_form.html'
    model = Address
    fields = '__all__'


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {'form': form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirct_path = next_ or next_post or None
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = request.POST.get('address_type', 'shipping')
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            print(address_type + "_address_id")

        else:
            print("some error")
            return redirect("carts:checkout")

        if is_safe_url(redirct_path, request.get_host()):
            return redirect(redirct_path)
        else:
            return redirect("carts:checkout")
    return redirect("carts:checkout")


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context = {}
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirct_path = next_ or next_post or None
        if request.method == 'POST':
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
            print(address_type + "_address_id")

            if is_safe_url(redirct_path, request.get_host()):
                return redirect(redirct_path)

    return redirect("carts:checkout")
