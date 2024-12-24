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

class Myview(View):
    gb = None
    gc = 0
    gpg = 4
    gbselectmenu = None
    globalpaginator = 6
    globalselectmenu = None
    globalcatid = 0
    globalpaginator1 = 8
    globalselectmenu1 = None
    globalpaginator2 = 4
    globalselectmenu2 = None
    globalpaginator3 = 4
    globalselectmenu3 = None
    # qadan alim


def index(request, ):
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    contex = {
        "setting": Setting.objects.get(pk=1),
        "slider_pk1": Slider.objects.get(pk=1),
        "slider_pk2": Slider.objects.get(pk=2),
        "slider_pk3": Slider.objects.get(pk=3),
        "slider_pk4": Slider.objects.get(pk=4),
        "slider_pk5": Slider.objects.get(pk=5),
        "slider_pk6": Slider.objects.get(pk=6),
        "slider_pk7": Slider.objects.get(pk=7),
        "slider_pk8": Slider.objects.filter(pk__range=(8, 16)),
        "category": Categories.objects.all(),
        "product": Product.objects.filter(sale='False').order_by('?')[:4],
        "product_sale": Product.objects.filter(sale='True').order_by('?')[:1],
        "product_new": Product.objects.filter(new='True').order_by('?')[:3],
        "product_kampaniya": Product.objects.filter(kampaniya='True').order_by('?')[:2]

    }
    return render(request, 'index/index.html', contex)


def contact(request):
    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile baglanti qur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız göndərildi. Təşəkkür edirik")

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    category = Categories.objects.all()
    contex = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'Contact/shop-contacts.html', contex)


def shopproductlist(request, id, slug):
    category_data = Categories.objects.get(pk=id)
    setting = Setting.objects.get(pk=1)
    categories = Categories.objects.all()
    product_queryset = Product.objects.filter(category_id=id)
    items_per_page = 6
    paginator = Paginator(product_queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "categorydata": category_data,
        "setting": setting,
        "category": categories,
        "page_obj": page_obj  # Pass the page object to the template
    }
    return render(request, 'Shop-product-list/shop-product-list.html', context)


def productinfo(request):
    contex = {
        "categorydata": Categories.objects.get(pk=id),
        "setting": Setting.objects.get(pk=1),
        "slider_pk1": Slider.objects.get(pk=1),
        "slider_pk2": Slider.objects.get(pk=2),
        "slider_pk3": Slider.objects.get(pk=3),
        "slider_pk4": Slider.objects.get(pk=4),
        "category": Categories.objects.all(),
    }
    return render(request, '../templatas/partials/productinfo.html', contex)


def shopitem(request, id, slug):
    contex = {
        "setting": Setting.objects.get(pk=1),
        "category": Categories.objects.all(),
        "product": Product.objects.get(pk=id),
        "product_popular": Product.objects.filter(popular='True').order_by('?')[:1],
        "product_simple": Product.objects.filter(sale='False', popular='False').order_by('?')[:2],
        "product_sale": Product.objects.filter(sale='True', popular='False').order_by('?')[:1],
        "product_images": Images.objects.filter(product=id).order_by('?')[:3],
        "comment": Comment.objects.filter(product_id=id).order_by('-pk')[:2]
    }
    return render(request, 'Shop-Item/shop-item.html', contex)


@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip_address = request.META.get('REMOTE_ADDR')  # Corrected typo in 'REMOTE_ADDR'
            if form.cleaned_data['comment'] == "":
                messages.warning(request, "Mesajiniz gonderilmedi")
            else:
                data.save()
                messages.success(request, 'Mesajiniz gonderildi')
            return HttpResponseRedirect(url)  # Redirect to the last page

    messages.warning(request, "Mesajiniz gonderilmedi")
    return HttpResponseRedirect(url)

    # Ensure to pass appropriate 'context' variable to the render function
    return render(request, 'Shop-Item/shop-item.html', context)


# Sehifeye giren kimi
def search(request, ):
    prk = Product.objects.filter(kampaniya='True').order_by('?')[:5]
    if request.method == 'POST':
        query = request.POST['query']
        if request.POST['catid'] != '0':
            catid = request.POST['catid']
            Myview.gb = query  # globala gonderdim
            Myview.gc = catid
            category = Categories.objects.all()
            products = Product.objects.filter(title__icontains=query, category_id=catid)
            setting = Setting.objects.get(pk=1)
            # Get the product queryset
            product_queryset = Product.objects.filter(title__icontains=query, category_id=catid)
            # Number of products per page
            items_per_page = Myview.gpg
            # Create Paginator object
            paginator = Paginator(product_queryset, items_per_page)
            # Get the current page number from the request query parameters
            page_number = request.GET.get('page')
            # Get the page object for the requested page
            page_obj = paginator.get_page(page_number)
            context = {'products': products,
                       'category': category,
                       'setting': setting,
                       'page_obj': page_obj,
                       'prk': prk
                       }
            return render(request, 'Shop-search/search.html', context)
        elif query != "":
            Myview.gc = 0
            Myview.gb = query  # globala gonderdim
            category = Categories.objects.all()
            products = Product.objects.filter(title__icontains=query)
            setting = Setting.objects.get(pk=1)
            # Get the product queryset
            product_queryset = Product.objects.filter(title__icontains=query)
            # Number of products per page
            items_per_page = Myview.gpg
            # Create Paginator object
            paginator = Paginator(product_queryset, items_per_page)
            # Get the current page number from the request query parameters
            page_number = request.GET.get('page')
            # Get the page object for the requested page
            page_obj = paginator.get_page(page_number)
            context = {'products': products,
                       'category': category,
                       'setting': setting,
                       'page_obj': page_obj,
                       'prk': prk
                       }
            return render(request, 'Shop-search/search.html', context)
        else:
            return HttpResponseRedirect('/')
    else:
        # search sonradan
        if request.GET.get('selectpaginator') is None and Myview.gbselectmenu is None:
            query = Myview.gb  # globaldan cagirdim
            catid = Myview.gc
            categories = Categories.objects.all()
            setting = Setting.objects.get(pk=1)
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
                product_queryset = Product.objects.filter(title__icontains=query, )
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
                product_queryset = Product.objects.filter(title__icontains=query, category_id=catid)
            items_per_page = Myview.gpg
            paginator = Paginator(product_queryset, items_per_page)
            page_number = request.GET.get('page')
            # Get the page object for the requested page
            page_obj = paginator.get_page(page_number)
            context = {'products': products,
                       'category': categories,
                       'setting': setting,
                       'page_obj': page_obj,
                       'prk': prk
                       }
            return render(request, 'Shop-search/search.html', context)
        else:
            query = Myview.gb
            catid = Myview.gc
            if request.GET.get('selectmenu') is not None:
                Myview.gbselectmenu = request.GET.get('selectmenu')
            if Myview.gbselectmenu == 'cari':
                if catid == 0:
                    products = Product.objects.filter(title__icontains=query)
                    product_queryset = Product.objects.filter(title__icontains=query)
                else:
                    products = Product.objects.filter(title__icontains=query, category_id=catid)
                    product_queryset = Product.objects.filter(title__icontains=query, category_id=catid)
            elif Myview.gbselectmenu == 'ucuz':
                if catid == 0:
                    products = Product.objects.filter(title__icontains=query).order_by('price')
                    product_queryset = Product.objects.filter(title__icontains=query).order_by('price')
                else:
                    products = Product.objects.filter(title__icontains=query, category_id=catid).order_by('price')
                    product_queryset = Product.objects.filter(title__icontains=query, category_id=catid).order_by(
                        'price')
            elif Myview.gbselectmenu == 'baha':
                if catid == 0:
                    products = Product.objects.filter(title__icontains=query).order_by('-price')
                    product_queryset = Product.objects.filter(title__icontains=query).order_by('-price')
                else:
                    products = Product.objects.filter(title__icontains=query, category_id=catid).order_by('-price')
                    product_queryset = Product.objects.filter(title__icontains=query, category_id=catid).order_by(
                        '-price')
            elif Myview.gbselectmenu == 'reyting':
                if catid == 0:
                    products = Product.objects.filter(title__icontains=query).order_by('-comment__rate')
                    product_queryset = Product.objects.filter(title__icontains=query).order_by('-comment__rate')
                else:
                    products = Product.objects.filter(title__icontains=query, category_id=catid).order_by(
                        '-comment__rate')
                    product_queryset = Product.objects.filter(title__icontains=query, category_id=catid).order_by(
                        '-comment__rate')
            categories = Categories.objects.all()
            setting = Setting.objects.get(pk=1)
            if request.GET.get('selectpaginator') is not None:
                Myview.gpg = request.GET['selectpaginator']
            items_per_page = Myview.gpg
            # Create Paginator object
            paginator = Paginator(product_queryset, items_per_page)
            # Get the current page number from the request query parameters
            page_number = request.GET.get('page')
            # Get the page object for the requested page
            page_obj = paginator.get_page(page_number)
            context = {'products': products,
                       'category': categories,
                       'setting': setting,
                       'page_obj': page_obj,
                       'prk': prk
                       }
            return render(request, 'Shop-search/search.html', context)


def autocomplete(request):
    if 'term' in request.GET:
        categories = Categories.objects.all()
        qs = Product.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)
        return JsonResponse(titles, safe=False)
    return render(request, 'index/index')


def productrange(request):
    if request.GET.get('selectpaginator') != None and request.GET.get('selectmenu') != None and request.GET.get(
            'categorydata') is not "":
        catid = request.GET.get('categorydata')
        Myview.globalcatid = catid
    catid = Myview.globalcatid
    if request.GET.get('selectmenu') is not None:
        Myview.globalselectmenu = request.GET.get('selectmenu')
    if Myview.globalselectmenu == 'cari':
        products = Product.objects.filter(category_id=catid)
        product_queryset = Product.objects.filter(category_id=catid)
    elif Myview.globalselectmenu == 'ucuz':
        products = Product.objects.filter(category_id=catid).order_by('price')
        product_queryset = Product.objects.filter(category_id=catid).order_by('price')
    elif Myview.globalselectmenu == 'baha':
        products = Product.objects.filter(category_id=catid).order_by('-price')
        product_queryset = Product.objects.filter(category_id=catid).order_by('-price')
    elif Myview.globalselectmenu == 'reyting':
        products = Product.objects.filter(category_id=catid).order_by('-comment__rate')
        product_queryset = Product.objects.filter(category_id=catid).order_by('-comment__rate')
    categories = Categories.objects.all()
    setting = Setting.objects.get(pk=1)
    if request.GET.get('selectpaginator') is not None:
        Myview.globalpaginator = request.GET['selectpaginator']
    items_per_page = Myview.globalpaginator
    paginator = Paginator(product_queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': products,
               'category': categories,
               'setting': setting,
               'page_obj': page_obj,
               }
    return render(request, 'Shop-product-list/shop-product-list.html', context)


def newproduct(request):
    setting = Setting.objects.get(pk=1)
    if request.GET.get('selectpaginator') is None and Myview.globalselectmenu1 is None:

        products = Product.objects.filter(new='True')
        product_queryset = Product.objects.filter(new='True')

    else:
        if request.GET.get('selectpaginator') is not None:
            Myview.globalpaginator1 = request.GET.get('selectpaginator')
        if request.GET.get('selectmenu') is not None:
            Myview.globalselectmenu1 = request.GET.get('selectmenu')
        if Myview.globalselectmenu1 == 'cari':
            products = Product.objects.filter(new='True')
            product_queryset = Product.objects.filter(new='True')
        if Myview.globalselectmenu1 == 'ucuz':
            products = Product.objects.filter(new='True').order_by('price')
            product_queryset = Product.objects.filter(new='True').order_by('price')
        if Myview.globalselectmenu1 == 'baha':
            products = Product.objects.filter(new='True').order_by('-price')
            product_queryset = Product.objects.filter(new='True').order_by('-price')

        if Myview.globalselectmenu1 == 'reyting':
            products = Product.objects.filter(new='True').order_by('-comment__rate')
            product_queryset = Product.objects.filter(new='True').order_by('-comment__rate')

    categories = Categories.objects.all()
    items_per_page = Myview.globalpaginator1
    paginator = Paginator(product_queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': products,
               'category': categories,
               'setting': setting,
               'page_obj': page_obj,
               }
    return render(request, 'Shop-product-list/newproduct.html', context)


def campaign(request):
    setting = Setting.objects.get(pk=1)
    if request.GET.get('selectpaginator') is None and Myview.globalselectmenu1 is None:

        products = Product.objects.filter(kampaniya='True')
        product_queryset = Product.objects.filter(kampaniya='True')

    else:
        if request.GET.get('selectpaginator') is not None:
            Myview.globalpaginator2 = request.GET.get('selectpaginator')
        if request.GET.get('selectmenu') is not None:
            Myview.globalselectmenu2 = request.GET.get('selectmenu')
        if Myview.globalselectmenu2 == 'cari':
            products = Product.objects.filter(kampaniya='True')
            product_queryset = Product.objects.filter(kampaniya='True')
        if Myview.globalselectmenu2 == 'ucuz':
            products = Product.objects.filter(kampaniya='True').order_by('price')
            product_queryset = Product.objects.filter(kampaniya='True').order_by('price')
        if Myview.globalselectmenu2 == 'baha':
            products = Product.objects.filter(kampaniya='True').order_by('-price')
            product_queryset = Product.objects.filter(kampaniya='True').order_by('-price')

        if Myview.globalselectmenu2 == 'reyting':
            products = Product.objects.filter(kampaniya='True').order_by('-comment__rate')
            product_queryset = Product.objects.filter(kampaniya='True').order_by('-comment__rate')

    categories = Categories.objects.all()
    items_per_page = Myview.globalpaginator2
    paginator = Paginator(product_queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': products,
               'category': categories,
               'setting': setting,
               'page_obj': page_obj,
               }
    return render(request, 'Shop-product-list/campaign.html', context)


def saleproduct(request):
    setting = Setting.objects.get(pk=1)
    if request.GET.get('selectpaginator') is None and Myview.globalselectmenu1 is None:

        products = Product.objects.filter(sale='True')
        product_queryset = Product.objects.filter(sale='True')

    else:
        if request.GET.get('selectpaginator') is not None:
            Myview.globalpaginator3 = request.GET.get('selectpaginator')
        if request.GET.get('selectmenu') is not None:
            Myview.globalselectmenu3 = request.GET.get('selectmenu')
        if Myview.globalselectmenu3 == 'cari':
            products = Product.objects.filter(sale='True')
            product_queryset = Product.objects.filter(sale='True')
        if Myview.globalselectmenu3 == 'ucuz':
            products = Product.objects.filter(sale='True').order_by('price')
            product_queryset = Product.objects.filter(sale='True').order_by('price')
        if Myview.globalselectmenu3 == 'baha':
            products = Product.objects.filter(sale='True').order_by('-price')
            product_queryset = Product.objects.filter(sale='True').order_by('-price')

        if Myview.globalselectmenu3 == 'reyting':
            products = Product.objects.filter(sale='True').order_by('-comment__rate')
            product_queryset = Product.objects.filter(sale='True').order_by('-comment__rate')

    categories = Categories.objects.all()
    items_per_page = Myview.globalpaginator3
    paginator = Paginator(product_queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': products,
               'category': categories,
               'setting': setting,
               'page_obj': page_obj,
               }
    return render(request, 'Shop-product-list/saleproduct.html', context)

























