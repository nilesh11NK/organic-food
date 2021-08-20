"""organic_food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from app import views
admin.site.site_header = 'Organic Food'

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about/',views.about),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout),
    path('contact_us/',views.contact_us),
    path('gallery/',views.gallery),
    path('my_account/',views.my_account),
    path('shop_detail/',views.shop_detail,name='shop_detail'),
    path('shop/',views.shop,name='shop'),
    path('order/',views.order,name='order'),
    path('register/',views.register),
    path('login/',views.login,name='login'),
    path('logout/',views.logout),
    path('addtocart/<int:id>',views.addtocart,name='addtocart'),
    path('showcart/',views.showcart,name='showcart'),
    path('plus/<int:id>/',views.plus,name='plus'),
    path('minus/<int:id>/',views.minus,name='minus'),
    path('remove/<int:id>/',views.remove,name='remove'),
    path('payment/',views.payment,name='payment'),
    path('success/',views.payment_success,name='success'),
    path('invoice/',views.invoice,name='invoice'),
    path('forpass/',views.forpass,name='forpass'),
    path('msgotp/',views.msgotp,name='msgotp'),
    path('changepass/',views.changepass,name='changepass'),
    path('search/',views.search,name='search'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
