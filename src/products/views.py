from django.shortcuts import get_object_or_404,render
from .models import Product
# Create your views here.
def products(request):
    pro=Product.objects.all()
    name=None
    desc = None
    prcifrom=None
    prcito=None
    cs=None
    if 'cs' in request.GET:
        cs=request.GET['cs']
        if not cs:
            cs='off'


    if 'searchname' in request.GET:
        name=request.GET['searchname']
        if name:
            if cs=='on':
                pro=pro.filter(name__contains=name)
            else:
                pro = pro.filter(name__icontains=name)

    if 'searchdesc' in request.GET:
        desc = request.GET['searchdesc']
        if desc:
            if cs == 'on':
                pro = pro.filter(description__contains=desc)#description__icontains from the model
            else:
                pro = pro.filter(description__icontains=desc)#description__icontains from the model

    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET:
        prcifrom = request.GET['searchpricefrom']
        prcito = request.GET['searchpriceto']
        if prcito and prcifrom:
            if prcito.isdigit() and prcifrom.isdigit():
                pro=pro.filter(price__gte=prcifrom,price__lte=prcito)


    context={
        'products':pro

    }

    return render(request,'products/products.html',context)


def product(request,pro_id):
    context={

        'pro':get_object_or_404(Product,pk=pro_id)
    }
    return render(request,'products/product.html',context)


def search(request):
    return render(request,'products/search.html')