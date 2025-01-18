from django.contrib import admin
from .models import (
    Category,
    Product,
    Image,
    ProductFeatureName,
    ProductFeatherValue,
    FavoriteProduct,
    Tag,
    Review,
    ContactUs,
    Emails
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'parent')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'inventory', 'status', 'category', 'created', 'updated')
    list_filter = ('status', 'category', 'created', 'updated')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'is_main', 'created')
    list_filter = ('is_main', 'created')
    search_fields = ('product__name', 'title')


@admin.register(ProductFeatureName)
class ProductFeatureNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug', 'product__name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductFeatherValue)
class ProductFeatherValueAdmin(admin.ModelAdmin):
    list_display = ('feather_name', 'value', 'product')
    search_fields = ('feather_name__name', 'value')


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'name', 'email')


@admin.register(Emails)
class EmailsAdmin(admin.ModelAdmin):
    list_display = ['email']

