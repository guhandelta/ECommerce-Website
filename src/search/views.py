from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
# Create your views here.

#def get_context_data(self, *args, **kwargs):
#    context = super(SearchProductView, self).get_context_data(*args, **kwargs)
#    context['query']= self.request.GET.get('q')
#    return context
    #This entire block of code is to get the query *q* through context
    #Since templates already have the ability to to perform request.GET.q, this entire block is not necesssary
    #If this block is given here, request.GET.get(q) should be replaced by *query* as in context['query'], which will hold the-
    #- value passed through q, in view.html
    # The ability of the templates to do the request is provided by the template context processor, in the seting.py-
    # under the templates section

class SearchProductView(ListView):
    template_name = "search/view.html"

    #def get_context_data(self, *args, **kwargs):
    #    context = super(SearchProductView, self).get_context_data(*args, **kwargs)
    #    query = self.request.GET.get(q)        
    #    context['query'] = query
    #    #SearchQuery.objects.create(query=query)
    #    return context

    def get_queryset(self,*args,**kwargs):
        request=self.request
        method_dict = request.GET
        print(request.GET)
        query = method_dict.get('q', None) # method_dict['q] is an alternative and hrows a valu error if th 'q' does not exist
        print(query)
        if query is not None:
            return Product.objects.search(query)       
        return Product.objects.featured()
    