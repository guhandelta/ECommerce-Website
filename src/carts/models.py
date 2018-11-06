from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product #Product model

User = settings.AUTH_USER_MODEL #User model
# This user model is from django.contrib.auth --> Installed Apps 
# It goes off the same appl, even when the user model is customized

class CartManager(models.Manager):

    def new_or_get(self, request):#create a new one or the current one as per the session
        #request is passed in here to get the current session
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count()==1:
            new_obj = False
            cart_obj=qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj
    #These is an predefined method as
    # def get_or_create():
    #       return obj, True --> returning the object and whether or not it was created
    # This method new_or_get() is same as it is, but it is more about how it is done over here
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated(): #Associating the user to the cart, after authentication/login
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user        = models.ForeignKey(User, null=True, blank=True) #null,blank =true is for enabling unauthenticated users to add items to cart
    products    = models.ManyToManyField(Product, blank=True) #Blank denotes blank cart
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True) #When the cart was last updated
    timestamp   = models.DateTimeField(auto_now_add=True) #When the cart was created

    objects     = CartManager()

    def __str__(self):
        return str(self.id) #id of the cart
#Using signals, here to calculate the total of the cart
def m2m_changed_cart_receiver(sender, instance, action,  *args, **kwargs):#This fn will be called when the save button is clicked
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':

        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal +10
    else:
        instance.total = 0
        
pre_save.connect(pre_save_cart_receiver, sender=Cart)