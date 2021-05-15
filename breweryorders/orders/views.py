from django.shortcuts import render, get_object_or_404
from .models import Beer, Distribution, Stock
from cart.forms import CartAddProductForm


# Create your views here.
def beer_list(request):
    beers = Beer.objects.all()
    return render(request,
                  'orders/beer/list.html',
                  {'beers': beers})


def beer_detail(request, beer):
    beer = get_object_or_404(Beer,
                             name=beer)
    return render(request,
                  'orders/beer/detail.html',
                  {'beer': beer})


def stock_list(request):
    products = Stock.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'orders/stock/list.html',
                  {'stock': products,
                   'cart_product_form': cart_product_form})


def product_detail(request, id):
    product = get_object_or_404(Stock, id=id, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'orders/stock/product.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
