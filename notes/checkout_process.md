# Checkout Process

1. Cart -> Checkout View
	Functionlaities in the Checkout View
		- Login/Register or Enter Email Addess(Guest)
		- Shipping Address
		- Billing Info
			-- Billing Address
			-- Credit/Debit Card Payment

2. Billing App/Component
	- Billing Profile
		-- User/Email
		-- Generate Payment Processor Token (StripeJS or Braintree)

3. Orders App/Componwnt
	- Connecting Billing Profile
	- Shipping & Billing address
	- Connect to the Cart	
	- Order status --> Shipped/Cancelled?