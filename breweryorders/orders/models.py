from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Beer(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField(null=True)
    createdon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey(User, on_delete=models.PROTECT)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name + " - " + self.type

    def get_absolute_url(self):
        return reverse('orders:beer_detail', args=[self.name])


class Distribution(models.Model):
    PACKAGE_CHOICES = (
        ('butelka', 'Butelka'),
        ('keg', 'Keg'),
    )
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, related_name='beer_distribution')
    package = models.CharField(max_length=7, choices=PACKAGE_CHOICES, default='butelka')
    capacity = models.DecimalField(max_digits=5, decimal_places=2)
    boxquantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ('beer', 'package',)

    def __str__(self):
        return '{} / {} o pojemności {}l'.format(self.beer, self.package, self.capacity)


class Stock(models.Model):
    AVAILABLE_STATUS = (
        ('dostępne', 'Dostępne'),
        ('ostatnie_sztuki', 'Ostatnie sztuki'),
        ('niedostępne', 'Niedostępne')
    )
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='beer_stock')
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=AVAILABLE_STATUS, default="niedostępne")
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('distribution',)

    def __str__(self):
        return 'Zapas {}: {} sztuk'.format(self.distribution, self.quantity)

    def get_absolute_url(self):
        return reverse('orders:product_detail', args=[self.id])


class Lot(models.Model):
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='beer_lot')
    quantity = models.PositiveIntegerField()
    productiondate = models.DateField()

    class Meta:
        ordering = ('-productiondate',)

    def __str__(self):
        return 'Partia {} o dacie: {}'.format(self.distribution, self.productiondate)


class Order(models.Model):
    STATUS_CHOICES = (
        ('złożone', 'Złożone'),
        ('zrealizowane', 'Zrealizowane'),
        ('anulowane', 'Anulowane'),
    )
    createdon = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='Złożone')
    totalamount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ('-createdon',)

    def __str__(self):
        return 'Zamówienie {}'.format(str(self.id).zfill(8))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    distribution = models.ForeignKey(Distribution, on_delete=models.PROTECT, related_name='beer_order')
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-order', 'distribution',)

    def __str__(self):
        return '{} / {}'.format(self.order, self.distribution)

    def save(self, *args, **kwargs):
        try:
            stock = Stock.objects.get(distribution=self.distribution)
            if (stock.quantity < self.quantity):
                print("{} - za mało towaru w magazynie".format(self.distribution))
                return
            else:
                super(OrderItem, self).save(*args, **kwargs)
        except Stock.DoesNotExist:
            print("{} - brak towaru w magazynie".format(self.distribution))
            return

# Create your models here.
