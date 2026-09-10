from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from main import views as mv
from products import views as pv

products = [
    path('videocards/', pv.videocards),
    path('processors/', pv.processors),
    path('ram/', pv.ram),
    path('ssd/', pv.ssd),
    path('motherboards/', pv.motherboards),
    path('powersupplies/', pv.powersupplies),
    path('cooling/', pv.cooling),
    path('cases/', pv.cases),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', mv.index),
    path('about/', mv.about),
    path('contacts/', mv.contacts),
    
    # Sign routes
    path('sign-in/', mv.sign_in),
    path('sign-in-2/', mv.try_sign_in),
    path('sign-up/', mv.sign_up),
    path('sign-up-2/', mv.try_sign_up),
    path('sign-out/', mv.sign_out),

    path('user-data/', mv.user_data),
    path('cart/', mv.cart_view, name='cart'),
    path('products/', include(products)),
    path('put-to-cart/<int:product_id>/', pv.put_to_cart, name='put_to_cart'),
    path('del-from-cart/<int:product_id>/', pv.del_from_cart, name='del_from_cart'),
    path('remove-from-cart/<int:product_id>/', pv.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', pv.clear_cart, name='clear_cart'),     
]