from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("shop-contact", views.contact, name="contact"),
    path('shop-product-list/<int:id>/<slug:slug>/', views.shopproductlist, name="shop-product-list"),
    path('productinfo', views.productinfo, name="productinfo"),
    path('shop-item/<int:id>/<slug:slug>/', views.shopitem, name="shop-item"),
    path('addcomment/<int:id>', views.addcomment, name="addcomment"),
    path("search/", views.search, name="search"),
    path('autocomplete', views.autocomplete, name="autocomplete"),
    path('productrange/', views.productrange, name="productrange"),
    path('newproduct/', views.newproduct, name="newproduct"),
    path('campaign/', views.campaign, name="campaign"),
    path('saleproduct/', views.saleproduct, name="saleproduct"),





]