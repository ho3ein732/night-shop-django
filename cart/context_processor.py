from .cart import Cart
from store.models import Product


def cart(request):
    return {'cart': Cart(request)}


def productss(request):
    return {'productss': Product.objects.all()}


def new_product(request):
    return {'new_product': Product.objects.all().order_by('-created')}


def top_sell(request):
    return {'top_sell': Product.objects.all().order_by('-sell')}