from django.shortcuts import render
#show the products card in the index padge
from django.http import HttpResponse
from products.models import Product

# Create your views here.
def index(request):
    context = {
        'products': Product.objects.all()

    }

    return render(request,'pages/index.html',context)
def about(request):
    return render(request,'pages/about.html')
def coffee(request):
    return render(request,'pages/coffee.html')