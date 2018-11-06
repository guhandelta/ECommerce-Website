Microsoft Windows [Version 10.0.17134.285]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Users\guhan>cd c:\DjangoProjects\ecommerce\src

c:\DjangoProjects\ecommerce\src>python manage.py startapp tags
2p9tqeln6i
rs4vckz5ui4zoyouk9jxyic6c7fffmtqi88cfdq97lhs705ce5

c:\DjangoProjects\ecommerce\src>python manage.py makemigrations
s1ayzdwdzc
pukqve9xpbh4086mlc9ymffswljvnkl6s3lu0rqt2qjquz5or2
Migrations for 'tags':
  tags\migrations\0001_initial.py
    - Create model Tag

c:\DjangoProjects\ecommerce\src>python manage.py migrate
12lmg2qnrp
xqc8nu26f4xnhfa4337jb68rglwjwgh2s7nlmah9dire3c7suv
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, products, sessions, tags
Running migrations:
  Applying tags.0001_initial... OK

c:\DjangoProjects\ecommerce\src>python manage.py shell
ojj4nchlp8
nfho88aqe4imox9qky5txo89zrf9asvws9kboyipi3umkgxivk
Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
KeyboardInterrupt
>>> exit
Use exit() or Ctrl-Z plus Return to exit
>>> ^Z

now exiting InteractiveConsole...

c:\DjangoProjects\ecommerce\src>ls
'ls' is not recognized as an internal or external command,
operable program or batch file.

c:\DjangoProjects\ecommerce\src>cd
c:\DjangoProjects\ecommerce\src

c:\DjangoProjects\ecommerce\src>python manage.py shell
cpmsz74epj
8iijfaw7d95c7mgyqy1040dlza02sm16a15j2yso8npjdrsckt
Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from tags.models import Tag
>>> Tag.objects.all()
<QuerySet [<Tag: T shirt>, <Tag: Tshirt>, <Tag: T-shirt>, <Tag: Red>, <Tag: Black>]>
>>> Tag.objects.last()
<Tag: Black>
>>> black=Tag.objects.last()
>>> black.title
'Black'
>>> black.slug
'black'
>>> black.active
True
>>> black.products
<django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x000001EAB1250080>
>>> black.products.all()
<ProductQuerySet [<Product: T-Shirt>, <Product: Hat>, <Product: T-shirt>]>
>>>
>>> black.products.all().first()
<Product: T-Shirt>
>>> qs=Product.objects.all()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'Product' is not defined
>>> ^Z

now exiting InteractiveConsole...

c:\DjangoProjects\ecommerce\src>python manage.py shell
s5u4nc787s
0gmq2iotd4hgaolcf6qisyk1d8fg5af6rtwvcqns6jxhrz0v3d
Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> qs=Product.objects.all()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'Product' is not defined
>>> from products.models import Product
>>> qs=Product.objects.all()
>>> qs
<ProductQuerySet [<Product: T-Shirt>, <Product: Hat>, <Product: Supercomputer>, <Product: Lorem Ipsum>, <Product: T-shirt>]>
>>> qs.first()
<Product: T-Shirt>
>>> tshirt
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'tshirt' is not defined
>>> tshirt=qs.first()
>>> tshirt
<Product: T-Shirt>
>>> tshirt.title
'T-Shirt'
>>> tshirt.slug
't-shirt'
>>> tshirt.price
Decimal('39.99')
>>> tshirt.active
True
>>> tshirt.tag
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'Product' object has no attribute 'tag'
>>> tshirt.tags
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'Product' object has no attribute 'tags'
>>> tshirt.active
True
>>> tshirt.description
'This is a great T-Shirt. Buy It!!....'
>>> tshirt.tag_set
<django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x0000027C3DFD6780>
>>> tshirt.tag_set.filter(title__iexact='Black')
<QuerySet [<Tag: Black>]>
>>>