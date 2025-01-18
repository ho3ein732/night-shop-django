from .cart import Cart
from store.models import Product


def cart(request):
    return {'cart': Cart(request)}


def productss(request):
    return {'productss': Product.objects.all()}
