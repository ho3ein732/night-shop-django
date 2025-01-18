from django.contrib import admin
from .models import BlogCategory, Tag, BlogPost, BlogComment, BlogGallery


# مدل BlogCategory
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at', 'updated_at')


admin.site.register(BlogCategory, BlogCategoryAdmin)


# مدل Tag
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag, TagAdmin)


# مدل BlogPost
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'status')
    list_filter = ('status', 'category', 'created_at', 'published_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    # نمایش توضیحات هنگام ویرایش
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'tags', 'content', 'status',)
        }),
    )


admin.site.register(BlogPost, BlogPostAdmin)


# مدل BlogComment
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username', 'content')


admin.site.register(BlogComment, BlogCommentAdmin)


# مدل BlogGallery
class BlogGalleryAdmin(admin.ModelAdmin):
    list_display = ('post', 'image', 'created_at')
    search_fields = ('post__title',)
    list_filter = ('created_at',)


admin.site.register(BlogGallery, BlogGalleryAdmin)
