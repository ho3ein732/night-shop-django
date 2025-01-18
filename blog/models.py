from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=100, blank=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات دسته‌بندی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "دسته‌بندی بلاگ"
        verbose_name_plural = "دسته‌بندی‌های بلاگ"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="نام تگ")
    slug = models.SlugField(max_length=50, blank=True, verbose_name="اسلاگ")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان پست")
    slug = models.SlugField(max_length=200, blank=True, verbose_name="اسلاگ")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", verbose_name="نویسنده")
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name="posts",
                                 verbose_name="دسته‌بندی")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="تگ‌ها")
    content = models.TextField(verbose_name="محتوا")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انتشار", auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "پست بلاگ"
        verbose_name_plural = "پست‌های بلاگ"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name="کاربر")
    content = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_approved = models.BooleanField(default=False, verbose_name="تأیید شده")
    first_name = models.CharField(max_length=20)
    email = models.EmailField()
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']

    def __str__(self):
        return f"نظر توسط {self.user} روی {self.post}"


class BlogGallery(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="gallery", verbose_name="پست")
    image = models.ImageField(upload_to="blog_gallery/", verbose_name="تصویر")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="متن جایگزین")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "گالری تصویر"
        verbose_name_plural = "گالری تصاویر"

    def __str__(self):
        return f"تصویر برای {self.post.title}"
