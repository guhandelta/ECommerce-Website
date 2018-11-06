#from django.views import ListView
from django.http import Http404
from django.views.generic import ListView, DetailView # can also be given as from django.views.generic.list.ListView
from django.shortcuts import render, get_object_or_404

from carts.models import Cart
from .models import Product

# Create your views here.

                ### List View ###

class ProductFeaturedListView(ListView):
    template_name="products/list.html"

    def get_queryset(self, *args,**kwargs):
        request=self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
    template_name="products/featured-detail.html"
    queryset= Product.objects.all().featured()


    #def get_queryset(self, *args, **kwargs):
    #    request=self.request
    #    return Product.objects.featured()

class ProductListView(ListView): #Class Based View
    #queryset = Product.objects.all()
    template_name = "products/list.html"
    #The context:queryset is not visible in this page, so a context variable is created here 
    #This fn gets the context for any given querySet or whateevr view is being done 
    #Every single class based view has this method --> Happens by default
    #This is a replacement for contect to be repeated here and this is how the generic views or class based views do to remove repetitions
#    def get_context_data(self, *args, **kwargs):
#        context = super(ProductListView, self).get_context_data(*args, **kwargs)
#        #context[""] = 
#        print(context)
#        return context
    #*args will manage/hold --> get_context_data(abc, 123, something)
    #**kwargs(key word args) will manage/hold --> get_context_data(abc, 123, something, another=abc, abc=123)
    #These were not explicitly written and replaced by self, whihc relates to the instance

    def get_queryset(self, *args, **kwargs):
        request=self.request
        return Product.objects.all()

def product_list_view(request): # Function Based View 
    queryset = Product.objects.all()
    context ={       
        'object_list' : queryset
    }
    return render(request,"products/list.html",context)

                ### Detail View ###

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    #All the product/view related tasks can be done here, but to make ti=hings simple, it is handles in the cart app{cart_update}
    def get_object(self, *args, **kwargs): #This can be replaced by the get_queryset() in the class ProductListView,
       #-that is more robust as the model manager is used over there
       request = self.request
       slug = self.kwargs.get('slug') # *slug* is what that is given in the Regex in ur ls.py
       #instance = get_object_or_404(Product, slug=slug, active=True) 
       try:
           instance = Product.objects.get(slug=slug, active=True)
       except Product.DoesNotExist:
            raise Http404("Not Found...")
       except Product.MultipleObjectsReturned: 
           qs=Product.objects.filter(slug=slug, active=True)
           instance=qs.first()
       except:
           raise Http404("Uhhmm......")
       return instance 

class ProductDetailView(DetailView): #Class Based View 
    #queryset = Product.objects.all()
    template_name = "products/detail.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context
    
    def get_object(self, *args, **kwargs): #This can be replaced by the get_queryset() in the class ProductListView,
        #-that is more robust as the model manager is used over there
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't Exist")
        return instance

def product_detail_view(request, pk=None, *args, **kwargs): # Function Based View 
    #instance=Product.objects.get(pk=pk, featured=True) --> Roguhly as same as the get_queryset() in class ProductFeaturedListView
    #instance = Product.objects.get(pk=pk) #id - Every single Django object has a Primary key, which is also the id
    #instance = get_object_or_404(Product, pk=pk)
    #try: --> This block is quite as same as get_object_or_404()
    #    instance=Product.objects.get(id=pk)
    #except Product.DoesNotExist:
    #    print('No Product Here')
    #    raise Http404("Product doesn't Exist")
    #except:
    #    print('huh?')

    instance = Product.objects.get_by_id(pk)#Shortcut for the above if/else block
    #For this line to work, a cusom model mamnger shoudl be created or override the default mmodel manager(which is dont in models @ models.py)
    #print(instance)
    if instance is None:
        raise Http404("Product doesn't Exist")

    #This block is important for lookups
    #qs = Product.objects.filter(id=pk) #Here a queryset is called upon a Product model, it is done over a model beacause of objects
    #-filter() here is a model manager fn() that allows us to to do operation on queryset
    #An object is considered a Model Manager -->It helps the programmer to do things like a qs, like a get() on a the actual-
    #-model itself. Objects is a representative of a model manager 
    #print(qs) --> This block is really more important how we go a step further and turn e listview into a searchview
    #if qs.count() == 1: #exists() and count() are inbuilf queryset functions
    #    instance = qs.first()
    #else:
    #    raise Http404("Product is not available")

    
    context ={        
        'object' : instance 
    }
    return render(request,"products/detail.html",context)
