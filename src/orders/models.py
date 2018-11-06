from django.db import models
from django.db.models.signals import pre_save, post_save #post_save signal is/can be used here to make a customized receiver fn for the cart

from carts.models import Cart
from ecommerce.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
		('created', 'Created'), #Tuples ('db_stored_value','display_value')
		('paid', 'Paid'),
		('shipped', 'Shipped'),
		#('delivered', 'Delivered'),
		('refunded', 'Refunded'),
	)

#Order ID - -> Random, Unique
class Order(models.Model):
	order_id		= models.CharField(max_length=120, blank=True)
	#billing_profile = 
	#shipping_address
	#billing_address
	cart			= models.ForeignKey(Cart)
	status			= models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
	shipping_total  = models.DecimalField(default=3.99, max_digits = 100, decimal_places=2)
	total			= models.DecimalField(default=0.00, max_digits = 100, decimal_places=2)

	def __str__(self):
		return self.order_id

	def update_total(self): #This method is called when a cart changes he order size or when an order is created 
		cart_total = self.cart.total
		print(cart_total)
		shipping_total = self.shipping_total
		new_total = cart_total + shipping_total
		print(new_total)
		self.total = new_total
		self.save() 
		return new_total

def pre_save_create_order_id(sender, instance, *args, **kwargs):
	if not instance.order_id:
		instance.order_id = unique_order_id_generator(instance)
		#instance.save() #--> Since pre_save signal is used here

pre_save.connect(pre_save_create_order_id, sender=Order)

#Recursin Depth Error occurs if the signals are not handles properly  	

def post_save_cart_total(sender, instance, created, *args, **kwargs): #Calculating the cart total
	if not created: #If the cart is not created yet, it won't be having an order -> if cart not craeted, do the following	
		cart_obj = instance
		cart_total = instance.total
		cart_id = cart_obj.id
		qs = Order.objects.filter(cart__id=cart_id)#In the cart object there is related data, lookup by the id and get the cart_id
		if qs.count == 1: #Equvivalent to qs.exists() also checking if there is only 1 order for this(a) cart
			#update the orders to what they are
			order_obj = qs.first()
			order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
	print('post_save_order')
	print('Before if, created = %s' %created)
	print('Running')
	#instance.update_total()
	if created:
		print('if stmnt, created = %s' %created)
		print('Updating - - - > First')
		instance.update_total()
	else:
		print('else stmnt, created = %s' %created)
		print('2nd entry')
		#instance.update_total()
	#The total can be updated everytime the cart is saved, but it is not necessary as the total changes when he cart/order changes

post_save.connect(post_save_order, sender=Order) 