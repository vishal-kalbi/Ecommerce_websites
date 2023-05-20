from django.shortcuts import render,redirect
import random
from .models import *
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


def seller_index(request):
    try:
        u1=Seller.objects.get(email=request.session['seller_email'])
        s_l = SellerOrderHistory.objects.filter(product__seller = u1)
        return render(request,'selller.html',{'sellerdata':u1,"my_orders": s_l})
    except:
        return render(request,'seller_registration.html')

def seller_registration(request):
    if request.method=='GET':
        return render(request,'seller_registration.html')
    else:    
        try:
            u1 = Seller.objects.get(email = request.POST['email'])
            return render(request, 'seller_registraton.html', {'msg': 'Email Already Exists'})
        except:
            
            global c_otp, data_list
            c_otp = random.randint(1000,9999)
            data_list = [
                request.POST['full_seller_name'],
                request.POST['your_email'],
                request.FILES['your_picture'],
                request.POST['your_password'],
                request.POST['your_Gst_no']

            ]

            subject = 'Welcome to Ecommerce'
            msg = f'Your OTP is from ecommerce is {c_otp}'
            from_mail = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['your_email']]
            send_mail(subject, msg, from_mail, recipient_list)
            return render(request, 'seller_otp.html')
        
            
        # return render(request, 'seller_otp.html', {'smessage': 'Successfully created!!'})
        
def seller_profile(request):
    if request.method == 'GET':
        try:
            s1 = Seller.objects.get(email = request.session['seller_email'])
            # seller_f_obj = Seller(instance= s1)
            return render(request, 'seller_profile.html', {'sellerdata': s1})
        except:
            return redirect('seller_login')
    else:
        s1 = Seller.objects.get(email = request.session['seller_email'])
        s1.full_name = request.POST['full_name']
        s1.Gst_no = request.POST['Gst_no']
        s1.Picture = request.FILES['Picture']
        s1.save() #ye line pe se database mein value update hogi
        return redirect('seller_profile')
    

def add_product(request):
    try:
        u1 = Seller.objects.get(email = request.session['seller_email'])
        if request.method=="GET":
            return render(request,'add_product.html',{"sellerdata":u1})  
        else:
            Product.objects.create(
                name=request.POST['product_name'],
                des=request.POST['description'],
                pic=request.FILES['product_picture'],
                price=request.POST['product_price'],
                seller=u1 # s1 seller classs ka object h ye hame foreign key ki field me dena padta h
            ) 
            return render(request,"add_product.html",{"sellerdata":u1,"msg":"successfully  created"})
    except: 
        return redirect("seller_login")        

def seller_otp(request):
    
    if int(request.POST['seller_otp'])==c_otp:
        Seller.objects.create(
            full_name= data_list[0],
            email= data_list[1],
            # pic= data_list[2],
            password = data_list[3],
            gst_no= data_list[4]
        )
        return render(request,'seller_login.html')
    else:
        return render(request,'seller_otp.html',{"msg":"OTP is invalid"}) 


def seller_login(request):
    try:
        if request.method=='GET':
            
            return render(request,'seller_login.html')
        else:
            u1=Seller.objects.get(email=request.POST['seller_email'])
            if request.POST['seller_password'] == u1.password:
                request.session['seller_email'] = request.POST['seller_email']
                return redirect('seller_index')
            else:
                return render(request,'seller_login.html',{'msg':"Invalid Paaword"})            

    except:
        return render(request,'seller_login.html',{'msg':"Email does not exist"})

def seller_logout(request):
    del request.session['seller_email'] 
    return redirect('seller_login')       
   

    