from django.views import generic
from django.http import  Http404
from django.shortcuts import render, get_object_or_404
from .models import Product
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin
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

def product_list(request):
    queryset = Product.objects.all()
    context ={
        'object_list': queryset
    }
    return render(request,'products/product_list.html',context)

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



# class ProductDetailSlug(generic.DetailView):
#     model = Product
#     template_name = 'products/product_detail.html'
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductDetailSlug, self).get_context_data(*args, **kwargs)
    #     cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    #     context['cart'] = cart_obj
    #     print(f'cart:{cart_obj}')
    #     return context

def product_detail(request,pk=None,*args,**kwargs):
    # instance = Product.objects.get(pk=pk)
    # instance = get_object_or_404(Product, pk=pk)
    # try:
    #     isinstance=Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     print('no product here')
    #     raise Http404("Product doesn't exist " )
    # except:
    #     print('??')

    qs = Product.objects.filter(pk=pk)
    print(qs)
    if qs.exists() and qs.count() ==1:
        instance = qs.first()
    else:
        raise Http404('Product not exist')

    context ={
        'object': instance
    }
    return render(request,'products/product_detail.html',context)
