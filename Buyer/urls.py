from django.contrib import admin
from django.urls import path,include
from Buyer.views import *


urlpatterns = [ 
    path('',fun1,name='index'),
    # path('contact/',fun2,name='contact Us'),
    path('faqs/',faqs,name='faqs'),
    path('typography/',typography,name='typography'),
    path('about/',about,name='about'),
    path('contact/',contact , name='contact'),
    path('reg/',signin,name='sign'),
    path('login/',login,name='login'),
    path('logout/', logout, name='logout'),
    path('otp/', otp, name='otp'),
    path('add_to_cart/<int:pk>', add_to_cart, name='add_to_cart'),
    path('cart/>', cart, name='cart'),
    path('del_cart_row/<int:cid>', del_cart_row, name='del_cart_row'),
    path('start_payment/',homepage, name='start_payment'),
    
    path('start_payment/paymenthandler/', paymenthandler, name='paymenthandler')
]
