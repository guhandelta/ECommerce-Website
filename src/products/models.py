import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator
from django.urls import reverse
# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    #print(instance)
    #print(filename)
    #defining the filename to be stored in the media folder
    new_filename = random.randint(1,3190209312)
    #retrieving the file extension of the uploaded file, like .jpg/.png/.jpeg.....etc
    name, ext = get_filename_ext(filename)
    #constructing the entre filename, alogn with its extension
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext) # can use f'{new_filename}{txt}' in Python 3.6.x
    return "products/{new_filename}/{final_filename}".format(
            new_filename = new_filename,
            final_filename = final_filename
    )
    #Writing/defining a new file name for the uploaded file, is just to make sure there are no problems while retrieving from
    #-the db, like Eg: Names with -,_,. are a valid url, but names with spaces will end up in throwing an error
      

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query): #This now can be used at many places
        lookups = ( Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(tag__title__icontains=query) 
                )

        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self): #Overriding get_queryset()
        return ProductQuerySet(self.model, using=self._db)
    def all(self):#if a product is marked inactive, the generall all call(this fn call) will not be there- 
        #-the queryset will not be in there
        return self.get_queryset().active()
    def featured(self):
        return self.get_queryset().featured() #featured() can be used over here and featured() and features() work in junction

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) #self.get_queryset() gets the queryset and is filtered using the filter()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self .get_queryset().active().search(query)

class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)  
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    #ImageField will throw an error if any file other than an image is uploaded
    #It needs the Python image library - pillow to open and check to see if it is an image
    #null means, tha value can be empty in the db || blank is to say that it is not required in Django     
    #putting these 2 together is for backend{null} not to get mad and Django{blank} not ot get mad 
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects     = ProductManager() #This is not overriding and any defaults, but just extending to it
    
    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug":self.slug}) #This is exact same as one above, but "/products/{slug}/" is-
        #- reverse("detail"). The namespace is added to make sure the reverse call is actually unique to the model itself.
    def __str__(self):                                    
        return self.title

    @property
    def name(self):
        return self.title
    
                                #  /\
#pre_save means, it's gonna do something, before the Product || is saved into the db

def product_pre_save_receiver(sender, instance, *srgs, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance) # creating a unique slug as per the name of the product/instance
            
pre_save.connect(product_pre_save_receiver, sender=Product)