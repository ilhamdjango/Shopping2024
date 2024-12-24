from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path('addtocart/<int:id>', views.addtocart, name='addtocart'),
    path("shopcart/", views.shopcart, name="shopcart"),
    path('deletefromcart/<int:id>',views.deletefromcart, name='deletefromcart'),
    path("orderproduct/", views.orderproduct, name="orderproduct"),


]