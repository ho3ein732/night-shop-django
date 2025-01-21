from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from django_resized import ResizedImageField
from account.models import NightUser


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=30, verbose_name='اسلاگ')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children',
                               verbose_name='دسته بندی والد')

    description = models.TextField(blank=True, null=True, verbose_name='توضیحاتـ')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    file = ResizedImageField(verbose_name='عکس ها', upload_to='images/', force_format='PNG', quality=100, blank=True)

    def __str__(self):
        return f'category {self.name}'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['-name']
        indexes = [
            models.Index(fields=['name', 'slug']),
            models.Index(fields=['parent'])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام محصول')
    slug = models.SlugField(verbose_name='اسلاگ')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products',
                                 verbose_name='دسته بندی')
    description = models.TextField(verbose_name='توضیحات')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    discount = models.IntegerField(default=0, verbose_name='تخفیف')
    material = models.CharField(max_length=25, default='برنجی', verbose_name='حنس')
    inventory = models.IntegerField(default=0, verbose_name='تعداد موجودی')
    sell = models.IntegerField(default=0, verbose_name='تعداد فروش')
    weight = models.PositiveIntegerField(default=0, verbose_name='وزن')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تولید شده در')
    updated = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی در')
    status = models.BooleanField(default=True, verbose_name='وضیعت محصول')
    brand = models.CharField(max_length=25, default='night', verbose_name='برند')

    def __str__(self):
        return f'{self.name} - {self.price or self.price} تومان'

    class Meta:
        ordering = ['-created']

        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['created', 'updated']),
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['category'])
        ]

        verbose_name = 'مجصول'
        verbose_name_plural = 'محصولات'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if not (0 > self.off > 100):
            raise ValueError('تخفیف باید بین 0 تا 100 باشد')

    @property
    def is_new(self):
        return (now() - self.created) <= timedelta(days=30)

    @property
    def new_price(self):
        return self.price - (self.price * self.discount // 100)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='عکس محصول')
    file = ResizedImageField(verbose_name='عکس ها', upload_to='images/', size=[500, 500],
                             crop=['middle', 'center'], force_format='PNG', quality=100)
    title = models.CharField(max_length=25, blank=True, null=True, verbose_name='عنوان')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شد در')
    is_main = models.BooleanField(default=False, verbose_name='عکس اصلی')

    def __str__(self):
        return f'photo for {self.product.name} product'

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'عکس محصول'
        verbose_name_plural = 'عکس های محصولات'


class ProductFeatureName(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام ویزگی')
    slug = models.SlugField(verbose_name='اسلاگ')

    class Meta:
        verbose_name = 'ویزگی'
        verbose_name_plural = 'ویژگی ها'

    def __str__(self):
        return f' - {self.name}'


class ProductFeatherValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features',
                                verbose_name='نام محصول')
    value = models.CharField(max_length=255, verbose_name='مقدار ویژگی')
    feather_name = models.ForeignKey(ProductFeatureName, on_delete=models.CASCADE, related_name='feather_value',
                                     verbose_name='نام ویزگی')

    class Meta:
        verbose_name = 'مقدار ویزگی'
        verbose_name_plural = 'مقدار ویژگی ها'

    def __str__(self):
        return f'{self.feather_name.name} --> {self.value}'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(NightUser, on_delete=models.CASCADE, verbose_name='محصولات مورد علاقه')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='اضافه شده در')

    class Meta:
        verbose_name = 'محصوب'
        verbose_name_plural = 'محبوب ها'

    def __str__(self):
        return f'{self.user} saved the {self.product.name}'


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='نام تگ')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='اسلاگ')
    products = models.ManyToManyField(Product, related_name='tags', blank=True, verbose_name='محصول')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(NightUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} for {self.product.name}'

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'product')

        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class ContactUs(models.Model):
    user = models.ForeignKey(NightUser, on_delete=models.SET_NULL, related_name='contact_us', null=True, blank=True)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    content = models.TextField()

    def __str__(self):
        return f'{self.user} for {self.name}'


class Emails(models.Model):
    email = models.EmailField()


class Copen(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()
    max_uses = models.PositiveIntegerField(default=1)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def is_valid(self, user, total_price):
        if not self.status or now() > self.expiration_date:
            return False
        if UserCopenUsage.objects.filter(user=user, copen=self).count() > self.max_uses:
            return False
        return True


class UserCopenUsage(models.Model):
    user = models.ForeignKey(NightUser, on_delete=models.CASCADE)
    copen = models.ForeignKey(Copen, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Banner(models.Model):
    POSITION_CHOICES = [
        ('top', 'بالا'),
        ('middle', 'وسط'),
        ('button', 'پایین')
    ]

    title = models.CharField(max_length=55, verbose_name='عنوان')
    short_description = models.CharField(max_length=55,verbose_name='توضیح مختصر')
    status = models.BooleanField(default=False, verbose_name='وضیعت')
    position = models.CharField(choices=POSITION_CHOICES, max_length=25, default='top', verbose_name='مکان بنر')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['position'])
        ]

        verbose_name = 'بنر'
        verbose_name_plural = 'بنر ها'


class BannerImage(models.Model):
    title = models.CharField(max_length=25, blank=True, null=True, verbose_name='عنوان بنر')
    short_description = models.CharField(max_length=55, blank=True, null=True, verbose_name='توضیحات مختصر بنر')
    file = ResizedImageField(verbose_name='', upload_to='images/', force_format='PNG', quality=100)
    banner = models.ForeignKey(Banner, related_name='images', on_delete=models.CASCADE, verbose_name='بنر')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'تصویر بنر'
        verbose_name_plural = 'تصویر های بنر'
