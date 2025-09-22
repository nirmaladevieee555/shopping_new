from django.shortcuts import render,redirect
from .models import *
from shop.form import CustomUserForm
from django.contrib import messages

from django.http import JsonResponse

from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    products= Product.objects.filter(trending=1)
    return render(request, "shop/index.html",{"products": products})
def  cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html",{"cart": cart})

    else:
        return redirect("/")

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")



def add_to_cart(request):
    
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'product Already in cart '}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'product Added to cart '}, status=200)
                    else:
                        return JsonResponse({'status':'product stock not available '}, status=200)
        else:
            return JsonResponse({'status':'Login  to add card '}, status=200)
    
    else:
        return JsonResponse({'status':'Invalid  Access'}, status=200)



def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logged out successfully")
    return redirect("/")    

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method =='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not  None:
                login(request,user)
                messages.success(request,"logged in successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid user Name or Password")
                return redirect("/login")
        return render(request, "shop/login.html")

def register(request):
    form=CustomUserForm()
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration success you can login now....!")
            return redirect('/login')
    return render(request, "shop/register.html",{'form':form})

def collections(request):
    
    catagory = Catagory.objects.filter(status=0)
    return render(request, "shop/collections.html", {"category": catagory})

def collectionsview(request,name):
    if (Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request, "shop/products/index.html", {"products": products,"category_name":name})
    
    else:
        messages.warning(request,"no such catagory  fount")
        return redirect('collections')
    
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_detail.html",{"products":products})

        else:
            messages.error(request,"no such catagory found")
            return redirect('collections')
    else:
        messages.error(request,"no such catagory found")
        return redirect('collections')
 
        




    




