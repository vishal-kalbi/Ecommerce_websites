from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.core.mail import send_mail
import random
from django.conf import settings
from seller.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
def fun1(request):
    p_list=Product.objects.all()
    try:
        u2=Buyer.objects.get(email=request.session['email'])
        return render(request,'index.html',{'change':u2, "products":p_list})
    except:
        return render(request,'index.html')    
def about(request):
    return render(request,'about.html')
def fun3(request):
    return render(request,'product.html')
def faqs(request):
    return render(request,'faqs.html')
def contact(request):
    return render(request,'contact.html')
def typography(request):
    return render(request,'typography.html')
def otp(request):
    if int(request.POST['otp'])==c_otp:
        Buyer.objects.create(
            first_name= data_list[0],
            last_name= data_list[1],
            email= data_list[2],
            address = data_list[3],
            password= data_list[4]
        )
        return render(request,'register.html')
    else:
        return render(request,'otp.html',{"msg":"OTP is invalid"})    
def login(request):
    try:
        if request.method=='GET':
            
            return render(request,'login.html')
        else:
            u1=Buyer.objects.get(email=request.POST['email'])
            if request.POST['password'] == u1.password:
                request.session['email'] = request.POST['email']
                return redirect('index')
            else:
                return render(request,'login.html',{'msg':"Invalid Paaword"})            

    except:
        return render(request,'login.html',{'msg':"Email does not exist"})            

def signin(request):
    
    if request.method=="GET":
        
        return render(request, 'register.html')
    else:
        
         
        try:
            u1 = Buyer.objects.get(email = request.POST['email'])
            return render(request, 'register.html', {'msg': 'Email Already Exists'})
        except:
            
            global c_otp, data_list
            c_otp = random.randint(1000,9999)
            data_list = [
                request.POST['first_name'],
                request.POST['lastname'],
                request.POST['email'],
                request.POST['Address'],
                request.POST['password']

            ]
    
            s = 'Welcome to Ecommerce'
            m = f'Your OTP is {c_otp}'
            fm = settings.EMAIL_HOST_USER
            rl = [request.POST['email']]
            send_mail(s, m, fm, rl)
            return render(request, 'otp.html')
    
        
    return render(request, 'login.html', {'smessage': 'Successfully created!!'})

def logout(request):
    
    del request.session['email']
    return redirect('index')
def add_to_cart(request,pk):
    try:
        u1 = Buyer.objects.get(email = request.session['email'])
        p1 = Product.objects.get(id = pk)
        Cart.objects.create(
            #ForeignKey wali field hoti hai to obj dena hai
            buyer = u1, 
            product = p1
        )
        return redirect('index')
    except:
        return redirect('login')
def cart(request):
    # try:
    u1 = Buyer.objects.get(email = request.session['email'])
    c_list = Cart.objects.filter(buyer = u1) #cart ke table mein se sirf u1 ke rows ek iterable mein de degi
    global amount_rupee
    amount_rupee = 0
    for i in c_list:
        amount_rupee += i.product.price
    return render(request, 'cart.html', {'userdata': u1, 'cart_data': c_list, 'total_product': len(c_list), 'total_amount': amount_rupee})
    # except:
    #     return redirect('login')     

def del_cart_row(request, cid):
    c_obj = Cart.objects.get(id = cid)
    c_obj.delete() #cart ka ye get kiya hua row delete ho jaayega
    return redirect('cart')           
    
def homepage(request):
    currency = 'INR'
    amount = amount_rupee * 100 # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'pay.html', context=context)

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = amount_rupee * 100  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    #seller order table mein rows create karni hai

                    # cart mein se products delete kar rhe hai success payment pe
                    u1 = Buyer.objects.get(email = request.session['email'])
                    c_l = Cart.objects.filter(buyer = u1)
                    for i in c_l:
                        SellerOrderHistory.objects.create(
                            product = i.product,
                            buyer = u1
                        )
                        i.delete()
                    # render success page on successful caputre of payment
                    return HttpResponse('Success')
                except:
 
                    # if there is an error while capturing payment.
                    return HttpResponse('failed!!')
            else:
 
                # if signature verification fails.
                return HttpResponse('Failed!!')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

