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
    Emails,
    Copen,
    UserCopenUsage,
    Banner,
    BannerImage
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


@admin.register(Copen)
class CopenAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'status', 'expiration_date', 'created_at')
    search_fields = ('code',)
    list_filter = ('status', 'expiration_date')


@admin.register(UserCopenUsage)
class UserCopenUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'copen', 'created_at')
    search_fields = ('user__username', 'copen__code')


class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 1
    verbose_name = "تصویر بنر"
    verbose_name_plural = "تصاویر بنر"


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'position', 'created_at')
    list_filter = ('status', 'position', 'created_at')
    search_fields = ('title', 'short_description', 'status', 'position')
    ordering = ('-created_at',)
    inlines = [BannerImageInline]
    readonly_fields = ('created_at',)


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description')
    search_fields = ('title', 'short_description')
