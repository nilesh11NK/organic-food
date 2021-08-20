from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Registation(models.Model):
	name=models.CharField(max_length=10)
	lname=models.CharField(max_length=10)
	email=models.EmailField()
	password=models.CharField(max_length=10)

class Category(models.Model):
	c_name=models.CharField(max_length=20)
	def __str__(self):
		return self.c_name


class Product(models.Model):
	c_name=models.ForeignKey(Category,on_delete=models.CASCADE)	
	p_name=models.CharField(max_length=20)
	p_price=models.PositiveIntegerField()
	p_img=models.ImageField(upload_to="")
	p_dis=models.TextField(null=True)
	def __str__(self):
		return self.p_name
	
class Cart(models.Model):
	user=models.ForeignKey(Registation,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	p_qty=models.PositiveIntegerField()
	sub_total=models.PositiveIntegerField()

setp=(('Pending','Pending'),('Accepted','Accepted'),('Packing','Packing'),('Delivery','Delivery'))

class Order(models.Model):
	user=models.ForeignKey(Registation,on_delete=models.CASCADE,null=True)
	cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
	address=models.CharField(max_length=20)
	country=models.CharField(max_length=20)
	state=models.CharField(max_length=20)
	pincode=models.PositiveIntegerField()
	date=models.DateField(null=True)
	order_status=models.CharField(choices=setp,max_length=100,default='Pending')