from django.urls import path
from . import views
app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart-status/', views.cart_status, name='cart-status'),
    path('remove-item/', views.remove_item, name='remove-item'),
    path('detail/', views.cart_detail, name='cart-detail'),
    path('update-cart/', views.update_quantity, name='update-quantity'),
    path('invoice/', views.add_address, name='add-address'),
    path('order/<int:order_id>/', views.order, name='order'),
]