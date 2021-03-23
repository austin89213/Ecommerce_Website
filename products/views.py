from django.views import generic
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductFile
from orders.models import ProductPurchase
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from billing.models import BillingProfile
from django.contrib import messages
# Create your views here.


class ProductFeaturedList(generic.ListView):
    template_name = "products/product_list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetail(ObjectViewedMixin, generic.DetailView):
    template_name = "products/featured_detail.html"

    def get_queryset(self, *args, **kwargs):
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
        context = super(ProductList, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


class ProductDetail(ObjectViewedMixin, generic.DetailView):
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
        context = super(ProductDetail, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        product_bought = self.check_bought()
        if product_bought:
            context['bought'] = 'Purchased'
        return context

    def get_object(self):
        obj = super().get_object()
        obj.viewed()
        obj.save()
        return obj

    def get_ip_address(self):
        ip = object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return ip


import os
from wsgiref.util import FileWrapper
from django.conf import settings
from mimetypes import guess_type
from orders.models import ProductPurchase


class ProductDownloadView(generic.View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(
            pk=pk, product__slug=slug
        )  # == ProdcutFile.objects.filter(product=product_obj)
        if downloads_qs.count() != 1:
            raise Http404('Download not found')
        download_obj = downloads_qs.first()
        can_download = False
        user_ready = True
        if download_obj.user_required:
            if not request.user.is_authenticated:
                user_ready = False
        purchased_products = Product.objects.none()

        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to download this item")
            return redirect(download_obj.get_default_url())

        aws_filepath = download_obj.generate_download_url()
        print(aws_filepath)
        return HttpResponseRedirect(aws_filepath)

        # file_root = settings.PROTECTED_ROOT
        # filepath = download_obj.file.path
        # final_filepath = os.path.join(file_root,filepath) # where the file is sotred
        # with open(final_filepath,'rb') as f:
        #     wrapper = FileWrapper(f)
        #     mimetype = 'application/force-download'
        #     gussed_mimetype = guess_type(filepath)[0]
        #     if gussed_mimetype:
        #         mimetype = gussed_mimetype
        #
        #     response = HttpResponse(wrapper,content_type=mimetype)
        #     response['Content-Disposition'] = "attachment;filename=%s"%(download_obj.name)
        #     response['X-SendFile'] = str(download_obj.name)
        #     return response


class UserProductHistoryView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'products/user_product_history_viewd.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, return_model_queryset=True)

        return views


class UserProductHistoryPurchase(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'products/user_product_history_purchased.html'
    context_object_name = 'products_purchased'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
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
        product_refunded = ProductPurchase.objects.refunded().products_by_request(self.request
                                                                                 ).exclude(id__in=product_active)
        queryset = {'product_active': product_active, 'product_refunded': product_refunded}
        print(f'active:{product_active},refunded:{product_refunded}')
        return queryset


class LibraryView(LoginRequiredMixin, generic.ListView):
    template_name = 'products/library.html'
    model = Product

    def get_queryset(self):
        qs = ProductPurchase.objects.active().products_by_request(self.request).filter(is_digital=True)
        print(qs)
        return qs
