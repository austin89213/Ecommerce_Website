from django.views import generic
from django.http import  Http404
from django.shortcuts import render, get_object_or_404
from .models import Product
from orders.models import ProductPurchase
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from billing.models import BillingProfile

# Create your views here.

class ProductFeaturedList(generic.ListView):
    template_name = "products/product_list.html"
    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetail(ObjectViewedMixin,generic.DetailView):
    template_name = "products/featured_detail.html"
    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductList(generic.ListView):
    model = Product
    def check_bought(self):
        product_bought = False
        if self.request.user.is_authenticated:
            user_billing_profile = self.request.user.billing_profile
            if self.object.purchased.filter(billing_profile=user_billing_profile).count():
                product_bought = True
        return product_bought

    def get_context_data(self, *args, **kwargs):
        context = super(ProductList,self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context



class ProductDetail(ObjectViewedMixin,generic.DetailView):
    model = Product

    def check_bought(self):
        product_bought = False
        if self.request.user.is_authenticated:
            user_billing_profile = self.request.user.billing_profile
            if self.object.purchased.filter(billing_profile=user_billing_profile).count():
                product_bought = True
        print(f'bought?:{product_bought}')
        return product_bought

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetail,self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        product_bought = self.check_bought()
        if product_bought:
            context['bought'] = 'Purchased'
        return context



    def get_ip_address(self):
        ip = object_viewed_signal.send(instance.__class__,instance=instance,request=request)
        return ip


class UserProductHistoryView(LoginRequiredMixin,generic.ListView):
    model = Product
    template_name = 'products/user_product_history_viewd.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self,*args,**kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, return_model_queryset=True)

        return views


class UserProductHistoryPurchase(LoginRequiredMixin,generic.ListView):
    model = Product
    template_name = 'products/user_product_history_purchased.html'
    context_object_name = 'products_purchased'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self,*args,**kwargs):
        # billing_profile = self.request.user.billing_profile
        # product_bought = ProductPurchase.objects.by_request(self.request).filter(refunded=False)
        # product_refunded = ProductPurchase.objects.by_request(self.request).filter(refunded=True)
        # bought_ids = [x.product.id for x in product_bought]
        # refunded_ids = [x.product.id for x in product_refunded]
        # for num in bought_ids:
        #     if num in refunded_ids:
        #         refunded_ids.remove(num)
        # obj_bought = Product.objects.filter(pk__in=bought_ids)
        # obj_refunded = Product.objects.filter(pk__in=refunded_ids)
        # print(f'bought:{obj_bought},refunded:{obj_refunded}')
        product_active = ProductPurchase.objects.active().products_by_request(self.request)
        product_refunded = ProductPurchase.objects.refunded().products_by_request(self.request)
        queryset={'product_active':product_active,'product_refunded':product_refunded}
        return queryset

class LibraryView(LoginRequiredMixin,generic.ListView):
    template_name='products/library.html'
    model = Product
    def get_queryset(self):
        qs = ProductPurchase.objects.active().products_by_request(self.request).filter(is_digital=True)
        print(qs)
        return qs
