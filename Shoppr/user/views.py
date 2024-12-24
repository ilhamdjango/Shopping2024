from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from home.models import Setting, ContactFormMessage, ContactFormu, Slider,UserProfile
from shopapp.models import Product, Categories, Images, Comment, CommentForm
from order.models import ShopCart,ShopCartForm
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from order.models import Order,OrderProduct





# Create your views here.

class Myview(View):
    selectpaginator = 4



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "İstifadəçi adı və ya parol yalnışdır")
            return HttpResponseRedirect('login')

    category = Categories.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {
        'category': category,
        'setting': setting
    }
    return render(request, 'login/login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    form = SignUpForm()
    category = Categories.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {
        'category': category,
        'setting': setting,
        'form': form
    }
    # Mistake: Incorrect template name
    return render(request, 'login/register.html', context)


def my_account(request, id):
    user = get_object_or_404(User, pk=id)
    user_profile, created = UserProfile.objects.get_or_create(user_id=id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name_text')
        user.last_name = request.POST.get('last_name_text')
        user.email = request.POST.get('email_text')
        user.save()
        user_profile.phone = request.POST.get('phone_text')
        user_profile.country = request.POST.get('country_text')
        user_profile.city = request.POST.get('city_text')
        user_profile.adress = request.POST.get('address_text')
        user_profile.save()
    context = {

        "setting": Setting.objects.get(pk=1),
        "user_profile": user_profile,
        "category": Categories.objects.all(),
    }

    return render(request, 'login/my_account.html', context)


def my_account2(request, id):
    user = get_object_or_404(User, pk=id)
    user_profile, created = UserProfile.objects.get_or_create(user_id=id)

    if request.method == 'POST' and request.FILES.get('file'):
        user_profile.image = request.FILES['file']
        user_profile.save()

    context = {
        "setting": Setting.objects.get(pk=1),
        "user_profile": user_profile,
        "category": Categories.objects.all(),
    }

    return render(request, 'login/my_account.html', context)




@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        current_user = request.user

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, 'Parol uğurla dəyişdirildi')
            return HttpResponseRedirect('password')
        else:
            messages.error(request, 'Yalnışdır')
            return HttpResponseRedirect('password')
    else:
        setting= Setting.objects.get(pk=1)
        category = Categories.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'login/change_password.html', {
            'form': form,
            'category': category,
            'setting':setting

        })


@login_required(login_url='/login')
def orders(request):
    category = Categories.objects.all()
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    orders = Order.objects.filter(user_id=current_user)

    if request.method == 'POST':
        selectpaginator = request.POST.get('selectpaginator')
        request.session['selectpaginator'] = selectpaginator
    else:
        selectpaginator = request.session.get('selectpaginator', 4)  # Default to 4 if not set

    paginator = Paginator(orders, selectpaginator)  # Paginate orders
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'orders': orders,
        "page_obj": page_obj,
        "setting": setting
    }
    return render(request, 'orders/orders.html', context)

@login_required(login_url='/login')
def orderdetail(request, id):
    category = Categories.objects.all()
    current_user = request.user
    setting = get_object_or_404(Setting, pk=1)
    order = get_object_or_404(Order, user_id=current_user.id, id=id)
    order_items = OrderProduct.objects.filter(order_id=id)
    user_profile = get_object_or_404(UserProfile, user_id=current_user.id)
    if request.method == 'POST':
        selectpaginator = request.POST.get('selectpaginator')
        request.session['selectpaginator'] = selectpaginator
    else:
        selectpaginator = request.session.get('selectpaginator', 4)  # Default to 4 if not set
    orders = Order.objects.filter(user_id=current_user.id)
    paginator = Paginator(order_items, selectpaginator)  # Paginate orders
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'order': order,
        'orderitems': order_items,
        'user_profile': user_profile,
        'setting': setting,
        'page_obj': page_obj,
    }
    return render(request, 'orders/user_orders.html', context)

@login_required(login_url='/login')
def comments(request):
    category = Categories.objects.all()
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    comments=Comment.objects.filter(user_id=current_user.id)

    if request.method == 'POST':
        selectpaginator = request.POST.get('selectpaginator')
        request.session['selectpaginator'] = selectpaginator
    else:
        selectpaginator = request.session.get('selectpaginator', 4)  # Default to 4 if not set

    paginator = Paginator(comments, selectpaginator)  # Paginate orders
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'comments': comments,
        "page_obj": page_obj,
        "setting": setting
    }
    return render(request, 'orders/comments.html', context)





@login_required(login_url='/login')
def deletecomment(request, id):
    current_user=request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.error(request,'Comment deleted..')
    return HttpResponseRedirect('/user/comments')






