from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#def my_home(request):
 #return render(request, 'home/home.html')

class ProductView(View):
 def get(self,request):
  sandwitch_maker = Product.objects.filter(category='SM')
  hand_blender = Product.objects.filter(category='HB')
  dry_irons = Product.objects.filter(category='DI')
  juicers = Product.objects.filter(category='J')
  mixers_grinders = Product.objects.filter(category='MG')
  food_processor = Product.objects.filter(category='FP')
  electric_kettel = Product.objects.filter(category='EK')
  return render(request, 'home/home.html',
  {'sandwitchmaker':sandwitch_maker, 'handblender':hand_blender,
  'dryirons':dry_irons, 'juicers':juicers, 'mixergrinders':mixers_grinders, 
  'foodprocessor':food_processor, 'electrickettel':electric_kettel})


def my_about(request):
 return render(request, 'home/about.html') 

#def profile(request):
 #return render(request, 'home/profile.html')










@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'home/orders.html', {'order_placed':op})

 






@login_required
def add_to_cart(request):
 user=request.user    
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')






@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user 
  cart = Cart.objects.filter(user=user) 
  amount = 0.0
  shipping_amount = 70.0
  totalamount=0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  #print(cart_product)
  if cart_product:
   for p in cart_product:
     tempamount = (p.quantity * p.product.selling_price)
     amount += tempamount
     totalamount = amount + shipping_amount
   return render(request, 'home/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount}) 
  else:
    return render(request, 'home/emptycart.html')








def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount= 70.0
    cart_product = [p for p in Cart.objects.all() if p.user ==  request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.selling_price)
      amount += tempamount
     


    data = {
     'quantity':c.quantity,
     'amount':amount,
     'totalamount':amount + shipping_amount
    }
    return JsonResponse(data)
  








def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount = 0.0
    shipping_amount= 70.0
    cart_product = [p for p in Cart.objects.all() if p.user ==  request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.selling_price)
      amount += tempamount
     


    data = {
     'quantity':c.quantity,
     'amount':amount,
     'totalamount':amount + shipping_amount
    }
    return JsonResponse(data)
  


def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount= 70.0
    cart_product = [p for p in Cart.objects.all() if p.user ==  request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.selling_price)
      amount += tempamount
      


    data = {
     'amount':amount,
     'totalamount':amount + shipping_amount
    }
    return JsonResponse(data)
  







#def customerregistration(request):
 #return render(request, 'home/customerregistration.html') 

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'home/customerregistration.html', {'form': form})


 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'home/customerregistration.html', {'form': form})

    

@login_required
def address(request):
  add = Customer.objects.filter(user=request.user)
  return render(request, 'home/address.html', {'add':add, 'active':'btn-primary'})
  
 





@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=request.user)
 amount = 0.0
 shipping_amount= 70.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user ==  request.user]
 if cart_product:
  for p in cart_product:
    tempamount = (p.quantity * p.product.selling_price)
    amount += tempamount
  totalamount = amount + shipping_amount  
 return render(request, 'home/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items}) 






@login_required
def payment_done(request):
 user = request.user 
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user = user)
 for c in cart:
   OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
   c.delete()
 return redirect("orders")






#def product_detail(request):
 #return render(request, 'home/productdetail.html')







class ProductDetailView(View):
 def get(self, request, pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  print(product.id)
  item_already_in_cart=False
  if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'home/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem}) 







def buy_now(request):
 return render(request, 'home/buynow.html') 

def services(request):
 return render(request, 'home/services.html')

def contactus(request):
 return render(request, 'home/contactus.html') 


def dry_irons(request, data=None):
 if data == None:
  dry_irons = Product.objects.filter(category='DI') 
 return render(request, 'home/dryirons.html', {'dry_irons':dry_irons}) 


def sandwitch_maker(request, data=None):
 if data == None:
  sandwitch_maker = Product.objects.filter(category='SM') 
 return render(request, 'home/sandwitchmaker.html', {'sandwitch_maker':sandwitch_maker}) 


def hand_blender(request, data=None):
 if data == None:
  hand_blender = Product.objects.filter(category='HB') 
 return render(request, 'home/handblender.html', {'hand_blender':hand_blender}) 


def juicers(request, data=None):
 if data == None:
  juicers = Product.objects.filter(category='J') 
 return render(request, 'home/juicers.html', {'juicers':juicers}) 


def mixers_grinders(request, data=None):
 if data == None:
  mixers_grinders = Product.objects.filter(category='MG') 
 return render(request, 'home/mixersgrinders.html', {'mixers_grinders':mixers_grinders})  


def food_processor(request, data=None):
 if data == None:
  food_processor = Product.objects.filter(category='FP') 
 return render(request, 'home/foodprocessor.html', {'food_processor':food_processor})  


def electric_kettel(request, data=None):
 if data == None:
  electric_kettel = Product.objects.filter(category='EK') 
 return render(request, 'home/electrickettel.html', {'electric_kettel':electric_kettel})   







@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'home/profile.html', {'form':form, 'active':'btn-primary'})  

 
 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user 
   name  = form.cleaned_data['name']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   reg = Customer(user=usr, name=name, city=city, state=state)
   reg.save()
   messages.success(request, 'Congratulations!! Profile Updated Successfully.')
   return render(request, 'home/profile.html', {'form':form, 'active':'btn-primary'})
 

