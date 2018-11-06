from django.shortcuts import render, redirect
from orders.models import Order
from products.models import Product
from .models import Cart

#def cart_create(user=None):
#    cart_obj = Cart.objects.create(user=None)
#    print('New Cart Created')
#    return cart_obj

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    #cart_id = request.session.get("cart_id", None) 
    #getting the cart_id from the session - The number associated with teh obj(cart_obj) in the db
    #The good thing about the sessions here is, if a cart is created when the user is not logged in is held in the db and
    #- another new cart is not created when the user logs in and the cart created before the user login is displayed
    # if cart_id is None: #isinstance() --> Making sure that the obj is type of that class just checking if the cart_id is an integer, 
    #    #If there is not cart, create one an set it to the session
    #    cart_obj = cart_create()     
    #    request.session['cart_id'] = cart_obj.id #The created cart will remain in the session
    # else:#If a cart exists
    #     qs = Cart.objects.filter(id=cart_id)#making sure the cart exists
    # #The upper IF statement is not required, as the qs.count checks if the cart exists
    # if qs.count() == 1:
    #    print('Cart ID Exists')
    #    cart_obj = qs.first()#If the cart exists, the cart_obj is set to the 1st obj(which is the cart, as only one cart/cart_obj-
    #    #- can exist)
    #    if request.user.is_authenticated() and cart_obj.user is None:
    #        cart_obj.user = request.user
    #        cart_obj.save()
    # else:
    #    cart_obj = Cart.objects.new(user=request.user)
    #    request.session['cart_id'] = cart_obj.id #Having the cart in teh session it had been creaetd and also in the view-
    #- where it had been created
    #This section is not required as the receivers and signals configures in the cart models, are handling it 
    #products = cart_obj.products.all()
    #total =0
    #for x in products:
    #    total += x.price
    #print(total)
    #cart_obj.total = total
    #cart_obj.save()
    return render(request, "carts/home.html", {})#"cart": cart_obj})

def cart_update(request): #This view does the basic stuff of adding products into the cart
    #print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product is not available")
            return redirect("carts:home") # When this exception occurs the user is taken to the cart home with no update done on the cart
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj) #remove the product if it is already in the cart
        else:
            cart_obj.products.add(product_obj) # can also be given as cart_obj.products.add(product_id) => product_id can also be given
            #cart_obj.title= "add"
            #cart_obj.save()
            #These 2 lines are not needed as the signals using m2m_changed and pre_save_cart to execute that change(saving)
        request.session['cart_items'] = cart_obj.products.count()
    #return redirect(product_obj.get_absolute_url()) -->Redirect to the product's page
    return redirect("carts:home") #Whenever an action add/remove happens, redirect the user to the cart homepage

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("carts:home") #Redirect to cart home if the cart has been created/is empty, just to make sure- 
        #-the cart is not created in the checkout page
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj) #get_or_create() is the inbuilt one
    return render(request, "carts/checkout.html", {"object":order_obj})