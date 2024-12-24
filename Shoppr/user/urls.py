from django.urls import path
from . import views


urlpatterns = [
    path('logout/', views.logout_view, name="logout_view"),
    path('login/', views.login_view, name="login_view"),  # Corrected URL for login view
    path('register/', views.register_view, name="register_view"),
    path('my_account/<int:id>/', views.my_account, name="my_account"),  # Ensure trailing slashes
    path('my_account2/<int:id>/', views.my_account2, name="my_account2"),  # Ensure trailing slashes
    path('password/', views.change_password, name="change_password"),  # Ensure trailing slashes
    path('orders/', views.orders, name="orders"),  # Ensure trailing slashes
    path('comments/', views.comments, name="comments"),
    path('orderdetail/<int:id>/', views.orderdetail, name="orderdetail"),  # Ensure trailing slashes
    path('deletecomment/<int:id>/', views.deletecomment, name="deletecomment"),  # Ensure trailing slashes
]
