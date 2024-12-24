from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from order.models import ShopCart, ShopCartForm,Order,OrderProduct
from home.models import Setting, ContactFormMessage, ContactFormu, Slider,UserProfile
from shopapp.models import Product, Categories, Images, Comment, CommentForm
from django.db import transaction
from .forms import OrderForm
from django.utils.crypto import get_random_string



# Create your views here.
def index(request):
    return render(request,'order/order.html')

@login_required(login_url='/login')
def addtocart(request, id):
    url=request.META.get('HTTP_REFERER')
    current_user = request.user
    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1
    else:
        control =0
    if request.method=='POST':
        form=ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
                 data = ShopCart.objects.get(product_id=id)
                 data.quantity += form.cleaned_data['quantity']
                 data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
            request.session['cart_items'] =ShopCart.objects.filter(user_id=current_user.id).count()
            messages.success(request,"Məhsul səbətə əlavə edildi")
            return HttpResponseRedirect(url)
    if id:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.user_id=current_user.id
            data.product_id=id
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Məhsul səbətə əlavə edildi")
        return HttpResponseRedirect(url)

    messages.warning(request,"Xəta olusdu")
    return HttpResponseRedirect(url)



@login_required(login_url='/login')
def shopcart(request):
    category = Categories.objects.all()
    current_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    total=0
    shipping=3
    for rs in shopcart:
        total +=rs.product.price * rs.quantity
    if total >=100:
        shipping=0
    contex = {
        "shopcart": ShopCart.objects.filter(user_id=current_user.id),
        "setting": Setting.objects.get(pk=1),
        'category' : category,
        "product_new": Product.objects.filter(new='True').order_by('?')[:4],
        "total" : total,
        "shipping" : shipping,
        "atotal":total+shipping,
        "user_profile" :user_profile


    }
    return render(request,'shopcart/shopcart.html',contex)


@login_required(login_url='/login')
def deletefromcart(request, id):
    current_user=request.user
    ShopCart.objects.filter(id=id).delete()
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request,"Məhsul səbətdən silindi")
    return HttpResponseRedirect("/order/shopcart")


@login_required(login_url='/login')
@transaction.atomic
def orderproduct(request):
    category = Categories.objects.all()
    current_user = request.user


    # Get or create the user's profile
    user_profile, created = UserProfile.objects.get_or_create(user_id=current_user.id)

    # Get the user's shopping cart
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = shopcart.count()

    # Calculate total price and shipping
    total = sum(rs.product.price * rs.quantity for rs in shopcart)
    shipping = 0 if total >= 100 else 3

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save the order
            data = Order(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                phone=form.cleaned_data['phone'],
                country=form.cleaned_data['country'],
                user_id=current_user.id,
                total=total,
                ip=request.META.get('REMOTE_ADDR'),
                code=get_random_string(5).upper()
            )
            data.save()

            # Save the order details
            for rs in shopcart:
                product = Product.objects.get(id=rs.product_id)
                OrderProduct.objects.create(
                    order_id=data.id,
                    product_id=rs.product_id,
                    user_id=current_user.id,
                    quantity=rs.quantity,
                    price=rs.product.price,
                    amount=rs.product.price * rs.quantity
                )
                # Update product amount
                product.amount -= rs.quantity
                product.save()

            # Clear the shopping cart
            shopcart.delete()
            request.session['cart_items'] = 0
            messages.success(request, "Sifarişiniz tamamlanmışdır!")
            return render(request, 'order/order.html', {'ordercode': data.code, 'category': category, 'user_profile' : user_profile})
        else:
            messages.warning(request, form.errors)
            return redirect("/order/orderproduct")

    context = {
        "shopcart": shopcart,
        "setting": Setting.objects.get(pk=1),
        "category": category,
        "product_new": Product.objects.filter(new=True).order_by('?')[:4],
        "total": total,
        "shipping": shipping,
        "atotal": total + shipping,
        "user_profile": user_profile

    }
    return render(request, 'order/order.html', context)








