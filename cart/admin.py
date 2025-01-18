from django.contrib import admin
from .models import OrderItem, Order, Address


# Custom admin for Address
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city', 'detailed_address', 'postal_code')
    search_fields = ('user__username', 'first_name', 'last_name', 'city__name', 'province__name')
    list_filter = ('city', 'province')


# Inline admin for OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # تعداد فرم‌های اضافی در پنل ادمین


# Custom admin for Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'status', 'created', 'updated', 'paid')
    search_fields = ('buyer__username', 'buyer__email', 'address__detailed_address')
    list_filter = ('status', 'paid', 'created')
    date_hierarchy = 'created'
    inlines = [OrderItemInline]


# Custom admin for OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('orders', 'product', 'price', 'quantity', 'weight')
    search_fields = ('orders__buyer__username', 'product__name')
    list_filter = ('orders',)
