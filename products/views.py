from django.views import generic
from django.http import  Http404
from django.shortcuts import render, get_object_or_404
from .models import Product
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin
from django.contrib.auth.mixins import LoginRequiredMixin

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
    def get_context_data(self, *args, **kwargs):
        context = super(ProductList,self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context



class ProductDetail(ObjectViewedMixin,generic.DetailView):
    model = Product
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetail,self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    def get_ip_address(self):
        ip = object_viewed_signal.send(instance.__class__,instance=instance,request=request)
        return ip


class UserProductHistoryView(LoginRequiredMixin,generic.ListView):
    model = Product
    template_name = 'products/user_product_history.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self,*args,**kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, return_model_queryset=True)

        return views
