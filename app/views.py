from django.shortcuts import render,redirect
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth 
from .form import *
from .models import *
from django.contrib import messages
import razorpay
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import random


# Create your views here.
def index(request):
	cat=Category.objects.all()
	return render(request,'index.html',{'cat':cat})


def about(request):
	cat=Category.objects.all()
	return render(request,'about.html',{'cat':cat})

def cart(request):
	cat=Category.objects.all()
	return render(request,'cart.html',{'cat':cat})

def checkout(request):
	if request.method =="POST":

		user =  request.session['user']
		address =  request.POST['address']
		country =  request.POST['country']
		state =  request.POST['state']
		pincode =  request.POST['pincode']
		date=request.POST['date']
		user_info=Registation.objects.get(email=user)
		cart=Cart.objects.filter(user__id=user_info.id)
		for c in cart:
			obj=Order(user=user_info,cart=c,date=date,address=address,country=country,state=state,pincode=pincode)
			obj.save()
	
		return redirect('payment')
		
	cat=Category.objects.all()
	return render(request,'checkout.html',{'cat':cat})

def contact_us(request):
	cat=Category.objects.all()
	return render(request,'contact_us.html',{'cat':cat})

def gallery(request):
	cat=Category.objects.all()
	return render(request,'gallery.html',{'cat':cat})

def my_account(request):
	cat=Category.objects.all()
	return render(request,'my_account.html',{'cat':cat})

def shop_detail(request):
	cid =  request.GET.get("cid")
	cat=Category.objects.all()
	data =  Product.objects.get(pk=cid)
	return render(request,'shop_detail.html',{'cat':cat,'data':data})

def shop(request):
	cid =  request.GET.get("cid")
	cat=Category.objects.all()
	data =  Product.objects.filter(c_name__id=cid)
	return render(request,'shop.html',{'cat':cat,"data":data})



def login(request):
	cat=Category.objects.all()
	if request.method=='POST':
		email = request.POST['email']
		password=request.POST['password']
		error=None
		if email==email:
			user=Registation.objects.get(email=email)
			if user.password==password:
				request.session['user']=email
				return redirect("/")
			else:
				return render(request, "login.html", {'error': "Invalid Password"})
    		
		else:
			return render(request, "login.html", {'error': "Invalid Email_Id"})
	else:
    		return render(request,"login.html") 

def register(request):
	cat=Category.objects.all()

	if request.method =="POST":
		name =  request.POST['name']
		lname =  request.POST['lname']
		email =  request.POST['email']
		password =  request.POST['password']
		user=Registation(name=name,lname=lname,email=email,password=password)
		user.save()
		messages.success(request,'Registered Successfully')
		return redirect('/login')

	else:
		return render(request,"register.html")
		
def logout(request):
	if 'user' in request.session:
		del request.session['user']
	else:
		return redirect('/login')
	return redirect('/login')

def addtocart(request,id):
	cat=Category.objects.all()
	con={}
	if 'user' in request.session:
		user=request.session['user']
		us=Registation.objects.get(email=user)
		project=Product.objects.get(id=id)
		cartexist=Cart.objects.filter(product__p_name=project.p_name)
		qty=1
		if cartexist:
			return redirect('showcart')
		else:
			Cart(user=us,product=project,p_qty=qty,sub_total=project.p_price).save()
			return redirect('showcart')
		con['Cart']=Cart.objects.filter(user__email=us)
	return render(request,'cart.html',con)
    
def showcart(request):
	cat=Category.objects.all()
	con={}
	if 'user' in request.session:
		us = request.session['user']
		user = Registation.objects.get(email=us)
		c1 = Cart.objects.filter(user_id = user.id)
		list1 = []
		sub_total =0
		for i in c1:

			list1.append(i.product.p_price)
			sub_total+=i.sub_total
        
		l1 = sum(list1)
		con['Cart']=c1
		con['sub_total']=sub_total
		return render(request,'cart.html',con)
	else :
		return redirect('login')

def plus(request,id):
	v1=Cart.objects.get(id=id)
	total=v1.product.p_price
	v1.p_qty+=1
	v1.sub_total=total*v1.p_qty
	v1.save()
	return redirect('showcart')

def minus(reduest,id):
	i1=Cart.objects.get(id=id)
	total=i1.product.p_price
	i1.p_qty-=1
	i1.sub_total=total*i1.p_qty
	i1.save()
	return redirect('showcart')

def remove(request,id):
	c1=Cart.objects.filter(id=id)
	c1.delete()
	return redirect('showcart')

def order(request):
	user=request.session['user'] 
	data=Order.objects.filter(user__email=user)
	return render(request,'order.html',{"data":data})

def payment(request):
	con={}
	if 'user' in request.session:
		us = request.session['user']
		user = Registation.objects.get(email=us)
		c1 = Cart.objects.filter(user_id = user.id)
		list1 = []
		sub_total =0
		for i in c1:

			list1.append(i.product.p_price)
			sub_total+=i.sub_total
        
		l1 = sum(list1)
		con['Cart']=c1
		con['sub_total']=sub_total
	
	amount = sub_total*100 #100 here means 1 dollar,1 rupree if currency INR
	client = razorpay.Client(auth=('rzp_test_wLZHZJcAx14CMc','8dOdy43WOXhOH6SbXE2URedX'))
	response = client.order.create({'amount':amount,'currency':'USD','payment_capture':1})
	print(response)
	context = {'response':response,'amount':amount}
	return render(request,"payment.html",context)

@csrf_exempt
def payment_success(request):
    if request.method =="POST":
        print(request.POST)
        return render(request,'payment_success.html',{})
    return redirect('/')

def invoice(request):
	con={}
	if 'user' in request.session:
		us = request.session['user']
		user = Registation.objects.get(email=us)
		c1 = Cart.objects.filter(user_id = user.id)
		list1 = []
		sub_total =0
		for i in c1:

			list1.append(i.product.p_price)
			sub_total+=i.sub_total
        
		l1 = sum(list1)
		con['Cart']=c1
		con['sub_total']=sub_total
		con ['user']=Registation.objects.all()
		return render(request,'invoice.html',con)
	
def forpass(request):
	if request.method=='POST':
		eemail=request.POST['email']
		otp = random.randint(00000,99999)
		user = Registation.objects.get(email=eemail) 
		if user is not None:
			em = send_mail(
				'OTP verification',
				f'Your OTP:{otp}',
				'nilesh.parmar9924@gmail.com',
				[eemail],  
			)
			request.session['otp'] = otp
			request.session['user'] = user.email
			return redirect('msgotp')
		else:
			return render(request,'forgetpass.html')
	return render(request,'forgetpassword.html')

def msgotp(request):
    inotp = request.session['otp']
    if request.method == 'POST':
        otp = request.POST['ootp']
        if inotp == int(otp):
            return redirect('changepass')
        else:
            return redirect('msgotp')
    else:
        return render(request,'otp.html')

def changepass(request):
	if request.method=='POST':
		email=request.session['user']
		user=Registation.objects.get(email=email)
		if request.method=='POST':
			pass1=request.POST['pass1']

			pass2=request.POST['pass2']
			if pass1==pass2:
				user.password=pass2
				user.save()
				return redirect('login')
			else:
				return redirect('changepass')
		else:
			return redirect('msgotp')
	else:
		return render(request,'changepassword.html')

def search(request):
	if request.method=='GET':
		sch=request.GET['sch']
		prod=Product.objects.filter(p_name__icontains=sch)
	return render(request,'search.html',{'prod':prod,'search':sch})