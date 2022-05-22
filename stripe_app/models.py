from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    CURRENCY_TYPE_CHOICES = (
        ('usd', 'Доллар США'),
        ('rub', 'Российский рубль'),

    )
    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.CharField(verbose_name='Описание', max_length=240)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10,
                                validators=[MinValueValidator(0)])
    currency = models.CharField(verbose_name='Валюта', choices=CURRENCY_TYPE_CHOICES,
                                max_length=3, default='usd')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.price}-{self.currency}'


class Discount(models.Model):
    name = models.CharField(verbose_name='Название скидки', max_length=100)
    description = models.CharField(verbose_name='Краткое описание скидки', max_length=240)
    stripe_coupon_id = models.CharField(verbose_name='ID купона в системе Stripe', max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(verbose_name='Название налога', max_length=100)
    description = models.CharField(verbose_name='Краткое описание налога', max_length=240)
    stripe_tax_id = models.CharField(verbose_name='ID налога в системе Stripe', max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name='Товары', related_name='orders')
    discount = models.ForeignKey(Discount, verbose_name='Скидка', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='orders')
    tax = models.ManyToManyField(Tax, verbose_name='Налоги', blank=True, related_name='orders')
