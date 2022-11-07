from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

# def home(request):
#     return render(request,'home.html')

class ProductView(View):
    def get(self,request):
        totalitem = 0
        topwears = Product.objects.filter(category = 'TW')
        bottomwears = Product.objects.filter(category = 'BW')
        mobiles = Product.objects.filter(category = 'M')
        laptops = Product.objects.filter(category='L')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'home.html',
                      {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops, 'totalitem':totalitem})


# def product_detail(request):
#     return render(request,'product-detail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'product-detail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == 'Redmi' or data == 'Samsung' or data == 'Realme' or data == 'iQOO' or data == 'Motorola' or data == 'Tecno' or data == 'Poco' or data == 'OnePlus':
        mobiles = Product.objects.filter(category = 'M').filter(brand = data)
    elif data == 'below':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt = 10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gt = 10000)
    elif data == 'above2':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)
    return render(request,'mobile.html', {'mobiles':mobiles})

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category = 'L')
    elif data == 'Lenovo' or data == 'Asus' or data == 'Acer' or data == 'Hp':
        laptops = Product.objects.filter(category = 'L').filter(brand = data)
    elif data == 'below':
        laptops = Product.objects.filter(category = 'L').filter(discounted_price__lt = 50000)
    elif data == 'above':
        laptops = Product.objects.filter(category = 'L').filter(discounted_price__gt = 50000)
    elif data == 'above2':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=100000)
    return render(request,'laptop.html', {'laptops':laptops})

def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category = 'TW')
    elif data == 'Life' or data == 'The_Modern_Soul' or data == 'Amazon' or data == 'ENDEAVOUR' or data == 'Lee':
        topwears = Product.objects.filter(category = 'TW').filter(brand = data)
    elif data == 'below':
        topwears = Product.objects.filter(category = 'TW').filter(discounted_price__lt = 500)
    elif data == 'above':
        topwears = Product.objects.filter(category = 'TW').filter(discounted_price__gt = 500)
    elif data == 'above2':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=1000)
    return render(request,'topwears.html', {'topwears':topwears})

def bottomwear(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category = 'BW')
    elif data == 'KB_TEAM' or data == 'DOMYOS' or data == 'Ketch' or data == 'SOLOGNAC' or data == 'Lee':
        bottomwears = Product.objects.filter(category = 'BW').filter(brand = data)
    elif data == 'below':
        bottomwears = Product.objects.filter(category = 'BW').filter(discounted_price__lt = 500)
    elif data == 'above':
        bottomwears = Product.objects.filter(category = 'BW').filter(discounted_price__gt = 500)
    elif data == 'above2':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=1000)
    return render(request,'bottomwears.html', {'bottomwears':bottomwears})

@login_required
def add_to_cart(request):
    user = request.user
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
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
            return render(request, 'add-to-cart.html', {'carts':cart, 'totalamount':total_amount, 'amount':amount})
        else:
            return render(request, 'emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount':  amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def buy_now(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    return render(request, 'buy-now.html', {'add':add})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
    return render(request,'checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

def login(request):
    return render(request,'login.html')

# def customer_registration(request):
#     return render(request,'customer-registration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'customer-registration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'customer-registration.html', {'form':form})


# def profile(request):
#     return render(request,'profile.html')
@method_decorator(login_required, name='dispatch')
class CustomerProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'profile.html', {'form':form, 'active':'btn-primary'})

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'address.html', {'add':add, 'active':'btn-primary'})

@login_required
def order(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request,'order.html', {'order_placed':op})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("order")

def search(request):
    q = request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request,'search.html',{'data':data})






