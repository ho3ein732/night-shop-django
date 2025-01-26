from django.db import models
from account.models import NightUser
from store.models import Product


# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(NightUser, on_delete=models.CASCADE, related_name='address')
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    province = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    detailed_address = models.TextField()
    postal_code = models.CharField(max_length=11, validators=[])
    plaque = models.CharField(max_length=10)
    recipient_phone = models.CharField(max_length=11)
    note = models.CharField(max_length=125, blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} -> {self.detailed_address}'


# Orders


class Order(models.Model):
    class Status(models.TextChoices):
        ORDER_CONFIRMATION = 'تایید سفارش', "تایید سفارش"
        review_queue = 'در صف بررسی', "در صف بررسی"
        preparation = 'آماده‌سازی', "آماده‌سازی"
        Delivery_to_post = 'تحویل به پست', "تحویل به پست"

    buyer = models.ForeignKey(NightUser, on_delete=models.SET_NULL, null=True, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='address')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.ORDER_CONFIRMATION)

    class Meta:
        ordering = ['-updated']
        indexes = [
            models.Index(fields=['-updated'])
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum([item.get_cost() for item in self.items.all()])

    def get_post_cost(self):
        weight = sum([item.get_weight() for item in self.items.all()])
        if weight < 1000:
            return 50000
        else:
            return 150000

    def get_final_cost(self):
        return self.get_total_cost() + self.get_post_cost()


class OrderItem(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} * {self.quantity}'

    def get_cost(self):
        return self.quantity * self.price

    def get_weight(self):
        return self.quantity * self.weight
