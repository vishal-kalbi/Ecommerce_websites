"""
URL configuration for EcomSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from seller.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('seller_registration/',seller_registration, name = 'seller_registration'),
    path('', seller_index, name = 'seller_index'),
    path('seller_login/', seller_login, name = 'seller_login'),
    path('seller_logout/', seller_logout, name = 'seller_logout'),
    path('add_product/', add_product, name = 'add_product'),
    path('seller_profile/', seller_profile, name = 'seller_profile'),
    path('seller_otp/', seller_otp, name = 'seller_otp'),
    
    


]
# apkbrwptoziqtykj