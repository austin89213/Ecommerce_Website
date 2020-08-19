from django.db.models import Q
from django.shortcuts import render
from products.models import Product
from django.views import generic
# Create your views here.
class SearchProductList(generic.ListView):
    template_name = 'search/search_list.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data()
        context ['query'] = self.request.GET['q']
        return context

    def get_queryset(self,*args,**kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q',None) #is q not exist, set it default to None
        queryset = Product.objects
        if query is not None:
            return queryset.search(query)
        return queryset.none()
        '''
        __icontains = field contains something

        __iexact = field is exact something

        '''
