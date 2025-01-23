from .cart import Cart
from store.models import Product, FavoriteProduct


def cart(request):
    return {'cart': Cart(request)}


def productss(request):
    return {'productss': Product.objects.all()}


def new_product(request):
    return {'new_product': Product.objects.all().order_by('-created')}


def top_sell(request):
    return {'top_sell': Product.objects.all().order_by('-sell')}


def number_favorite(request):
    favorites = FavoriteProduct.objects.filter(user=request.user).count()
    return {'number_favorite': favorites}